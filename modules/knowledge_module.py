# knowledge_module.py
import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from langchain_openai import AzureOpenAIEmbeddings
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv

load_dotenv()

class KnowledgeModule:
    def __init__(self):
        self.chroma_client = None
        self.collection = None
        self.embeddings = None
        self.encoder_model = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize ChromaDB client, embeddings, and reranker"""
        try:
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path="./chroma-db")
            self.collection = self.chroma_client.get_or_create_collection(name="rag_collection")
            
            # Initialize Azure OpenAI embeddings
            self.embeddings = AzureOpenAIEmbeddings(
                azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
                openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                openai_api_version=os.getenv("AZURE_OPENAI_EMBEDDING_VERSION"),
            )
            
            # Initialize cross-encoder for reranking using local model
            local_model_path = "./Modal/ms-marco-MiniLM-L-6-v2"
            if os.path.exists(local_model_path):
                self.encoder_model = CrossEncoder(local_model_path, trust_remote_code=True, revision="main")
            else:
                # Fallback to online model if local doesn't exist
                self.encoder_model = CrossEncoder("ms-marco-MiniLM-L-6-v2", trust_remote_code=True, revision="main")
            
            logging.info("✅ Knowledge module initialized successfully")
        except Exception as e:
            logging.error(f"❌ Error initializing knowledge module: {str(e)}")
            raise
    
    def decompose_query(self, user_query: str) -> List[str]:
        """
        Decompose a complex user query into multiple simpler queries
        """
        # Simple decomposition logic - can be enhanced with more sophisticated NLP
        queries = []
        
        # Split by common conjunctions and punctuation
        import re
        split_patterns = [
            r'\s+and\s+', r'\s+or\s+', r'\s+but\s+', r'\s+however\s+',
            r'\s*;\s*', r'\s*\.\s*', r'\s*,\s*'
        ]
        
        current_query = user_query
        for pattern in split_patterns:
            parts = re.split(pattern, current_query, flags=re.IGNORECASE)
            if len(parts) > 1:
                current_query = parts[0]
                queries.extend([part.strip() for part in parts[1:] if part.strip()])
        
        # Add the main query
        if current_query.strip():
            queries.insert(0, current_query.strip())
        
        # If no decomposition occurred, return the original query
        if not queries:
            queries = [user_query]
        
        # Limit to reasonable number of queries
        return queries[:5]
    
    def search_vector_store(self, query: str, n_results: int = 5) -> List[str]:
        """
        Search the vector store for relevant documents
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding], 
                n_results=n_results
            )
            
            # Extract documents
            documents = results["documents"][0] if results["documents"] else []
            
            return documents
        except Exception as e:
            logging.error(f"❌ Error searching vector store: {str(e)}")
            return []
    
    def rerank_documents(self, documents: List[str], query: str) -> tuple[str, List[int]]:
        """
        Rerank documents using cross-encoder
        """
        try:
            if not documents:
                return "", []
            
            # Rerank using cross-encoder
            ranks = self.encoder_model.rank(query, documents, top_k=min(3, len(documents)))
            
            relevant_text = ""
            relevant_text_ids = []
            
            for rank in ranks:
                relevant_text += documents[rank["corpus_id"]] + "\n\n"
                relevant_text_ids.append(rank["corpus_id"])
            
            return relevant_text, relevant_text_ids
        except Exception as e:
            logging.error(f"❌ Error reranking documents: {str(e)}")
            return "\n\n".join(documents), list(range(len(documents)))
    
    def get_knowledge_context(self, user_query: str, previous_queries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Main function to get knowledge context from vector store
        """
        try:
            # Decompose the current query
            decomposed_queries = self.decompose_query(user_query)
            
            # Add previous queries if provided
            all_queries = decomposed_queries.copy()
            if previous_queries:
                all_queries.extend(previous_queries)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_queries = []
            for query in all_queries:
                if query not in seen:
                    seen.add(query)
                    unique_queries.append(query)
            
            # Search and rerank for each query
            all_relevant_text = []
            query_results = {}
            
            for query in unique_queries:
                # Search vector store
                documents = self.search_vector_store(query)
                
                if documents:
                    # Rerank documents
                    relevant_text, relevant_ids = self.rerank_documents(documents, query)
                    
                    all_relevant_text.append(relevant_text)
                    query_results[query] = {
                        "documents": documents,
                        "reranked_text": relevant_text,
                        "relevant_ids": relevant_ids
                    }
            
            # Combine all relevant text
            combined_context = "\n\n".join(all_relevant_text)
            
            return {
                "status": "success",
                "original_query": user_query,
                "decomposed_queries": decomposed_queries,
                "all_queries_processed": unique_queries,
                "combined_context": combined_context,
                "query_results": query_results,
                "total_documents_found": len([doc for result in query_results.values() for doc in result["documents"]])
            }
            
        except Exception as e:
            logging.error(f"❌ Error getting knowledge context: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "original_query": user_query,
                "combined_context": ""
            }
    
    def search_specific_topic(self, topic: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Search for a specific topic in the knowledge base
        """
        try:
            # Search vector store
            documents = self.search_vector_store(topic, n_results)
            
            if documents:
                # Rerank documents
                relevant_text, relevant_ids = self.rerank_documents(documents, topic)
                
                return {
                    "status": "success",
                    "topic": topic,
                    "documents_found": len(documents),
                    "relevant_text": relevant_text,
                    "document_ids": relevant_ids
                }
            else:
                return {
                    "status": "no_results",
                    "topic": topic,
                    "documents_found": 0,
                    "relevant_text": "",
                    "document_ids": []
                }
                
        except Exception as e:
            logging.error(f"❌ Error searching specific topic: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "topic": topic,
                "relevant_text": ""
            } 