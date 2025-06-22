# Knowledge Agent Integration

## Overview

The Knowledge Agent is a specialized AI assistant that connects to a ChromaDB vector store to provide comprehensive answers to user queries. It uses advanced query decomposition, vector search, and reranking to deliver detailed information from stored documentation.

## Features

### 🔍 **Query Decomposition**
- Automatically breaks down complex queries into multiple simpler queries
- Handles multi-part questions and compound queries
- Improves search accuracy by processing each component separately

### 🧠 **Vector Database Search**
- Connects to ChromaDB vector store for semantic search
- Uses Azure OpenAI embeddings for query encoding
- Retrieves relevant documents based on semantic similarity

### 📊 **Advanced Reranking**
- Uses Cross-Encoder (ms-marco-MiniLM-L-6-v2) for document reranking
- Ensures the most relevant information is presented first
- Improves answer quality through intelligent ranking

### 🔄 **Context Integration**
- Considers previous queries in the conversation
- Maintains conversation context for better relevance
- Provides coherent, contextual responses

## Architecture

```
User Query → Query Decomposition → Vector Search → Reranking → Context Integration → Final Answer
```

### Components

1. **KnowledgeModule** (`modules/knowledge_module.py`)
   - Core functionality for vector store operations
   - Query decomposition and processing
   - Document search and reranking

2. **Knowledge Agent** (`app/agent_instructions.py`)
   - Specialized agent instructions
   - Integration with the main agent system
   - Tool coordination and response formatting

3. **Agent Builder** (`app/agent_builder.py`)
   - Agent instantiation and configuration
   - Tool assignment and agent hierarchy

## Setup Requirements

### Dependencies
Add these to your `requirements.txt`:
```
chromadb
langchain-openai
sentence-transformers
PyMuPDF
```

### Environment Variables
Ensure your `.env` file contains:
```
AZURE_OPENAI_EMBEDDING_MODEL=your-embedding-model
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_EMBEDDING_VERSION=your-version
```

### ChromaDB Setup
1. Ensure your ChromaDB vector store is located at `./chroma-db`
2. The collection should be named `rag_collection`
3. Documents should be properly embedded and indexed

## Usage

### Basic Knowledge Queries
```
User: "What are the procedures for meal ordering in catering?"
Agent: [Searches knowledge base and provides comprehensive answer]
```

### Specific Topic Queries
```
User: "Tell me about stock count procedures"
Agent: [Searches for specific topic and provides detailed information]
```

### Complex Multi-part Queries
```
User: "What are the meal ordering procedures and how do they relate to flight scheduling and stock management?"
Agent: [Decomposes query, searches multiple aspects, provides comprehensive answer]
```

## Available Tools

### 1. `get_knowledge_context`
- **Purpose**: Main knowledge search function
- **Parameters**:
  - `user_query` (string, required): The user's query
  - `previous_queries` (list, optional): Previous conversation queries
- **Returns**: Comprehensive search results with context

### 2. `search_specific_topic`
- **Purpose**: Targeted topic search
- **Parameters**:
  - `topic` (string, required): Specific topic to search
  - `n_results` (integer, optional): Number of results (default: 3)
- **Returns**: Focused results for the specific topic

## Integration with Main System

The Knowledge Agent is integrated into the main agent hierarchy:

```
Root Agent (catering_agent_v2)
├── Greeting Agent
├── Farewell Agent
└── Main Multi Tool Agent
    ├── Flight Info Agent
    ├── Meal Order Agent
    ├── Meal Issue Agent
    ├── Stock Count Approver Agent
    └── Knowledge Agent ← NEW
```

### Agent Delegation
The main agent automatically delegates to the Knowledge Agent when:
- User asks for detailed explanations
- Queries require reference to documentation
- Complex information requests are made
- Policy or procedure questions are asked

## Testing

Run the test script to verify integration:
```bash
python test_knowledge_agent.py
```

This will test:
- Knowledge module initialization
- Query decomposition functionality
- Vector store connectivity
- Agent integration
- Tool availability

## Example Responses

### Knowledge Search Results Format
```
**Knowledge Search Results:**
- **Query Processed:** What are the meal ordering procedures?
- **Decomposed Queries:** ['meal ordering procedures', 'catering meal processes']
- **Documents Found:** 5
- **Search Results:** 
  [Comprehensive answer based on retrieved information including procedures, 
  policies, and guidelines from the knowledge base]
```

### Error Handling
- **No Results**: "I couldn't find specific information about this topic in our knowledge base."
- **Search Errors**: Provides helpful alternatives or asks for clarification
- **Partial Results**: Presents available information and acknowledges limitations

## Best Practices

### For Users
1. **Be Specific**: Ask detailed questions for better results
2. **Use Context**: Reference previous conversation for continuity
3. **Ask Follow-ups**: The agent can handle multi-turn conversations

### For Developers
1. **Monitor Performance**: Check search result quality and relevance
2. **Update Knowledge Base**: Regularly add new documents to ChromaDB
3. **Tune Parameters**: Adjust search and reranking parameters as needed

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Error**
   - Verify the path `./chroma-db` exists
   - Check if the collection `rag_collection` is created
   - Ensure documents are properly indexed

2. **Azure OpenAI Credentials Error**
   - Verify all environment variables are set correctly
   - Check API key validity and endpoint accessibility
   - Ensure embedding model is available

3. **No Search Results**
   - Check if the knowledge base contains relevant documents
   - Verify query decomposition is working correctly
   - Consider expanding the knowledge base with more content

### Debug Mode
Enable logging to debug issues:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Future Enhancements

1. **Enhanced Query Decomposition**: More sophisticated NLP for query breakdown
2. **Multi-modal Search**: Support for images and other media types
3. **Learning Capabilities**: Improve search based on user feedback
4. **Custom Embeddings**: Support for domain-specific embedding models
5. **Advanced Filtering**: Add metadata-based filtering capabilities

## Support

For issues or questions about the Knowledge Agent integration:
1. Check the test script output for diagnostic information
2. Verify all dependencies are installed correctly
3. Ensure ChromaDB and Azure OpenAI are properly configured
4. Review the agent instructions for proper usage patterns 