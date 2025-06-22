# Step 0: Imports and setup
import streamlit as st
import os
import logging
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
import fitz  # PyMuPDF
import chromadb
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import AzureOpenAIEmbeddings
from sentence_transformers import CrossEncoder

# === Step 1: Load environment variables from .env ===
if os.path.exists(".env"):
    load_dotenv(override=True)
    config = dotenv_values(".env")
else:
    raise FileNotFoundError("Missing .env file in the current directory.")

# Step 2: Helper to ensure required env vars are present
def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

# Step 3: Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"rag_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logging.info("🔵 App started.")

# Step 4: Streamlit UI setup
st.set_page_config(page_title="RAG with ChromaDB", layout="wide")
st.title("📄 Upload and Embed Files with ChromaDB")

# Step 5: Upload File
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"])

# Step 6: PDF Text Extractor
def extract_text_from_pdf(file) -> str:
    logging.info("📄 Extracting text from PDF...")
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for i, page in enumerate(doc):
        page_text = page.get_text()
        logging.info(f"Page {i + 1} extracted, {len(page_text)} characters.")
        text += page_text
    return text

# Step 6.1: Cross-encoder re-ranking
def re_rank_cross_encoders(documents: list[str], prompt: str) -> tuple[str, list[int]]:
    relevant_text = ""
    relevant_text_ids = []
    encoder_model = CrossEncoder("ms-marco-MiniLM-L-6-v2", trust_remote_code=True, revision="main")
    ranks = encoder_model.rank(prompt, documents, top_k=3)
    for rank in ranks:
        relevant_text += documents[rank["corpus_id"]] + "\n\n"
        relevant_text_ids.append(rank["corpus_id"])
    return relevant_text, relevant_text_ids

# Step 7: Process Uploaded File
if uploaded_file:
    st.success("✅ File uploaded")
    logging.info(f"📂 File uploaded: {uploaded_file.name}")

    # Extract text from file
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")
    logging.info(f"✅ Text extracted from file, total {len(text)} characters.")

    # Step 8: Initialize Azure OpenAI Embeddings
    logging.info("🧠 Initializing Azure OpenAI embeddings...")
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=get_env_var("AZURE_OPENAI_EMBEDDING_MODEL"),
        openai_api_key=get_env_var("AZURE_OPENAI_API_KEY"),
        azure_endpoint=get_env_var("AZURE_OPENAI_ENDPOINT"),
        openai_api_version=get_env_var("AZURE_OPENAI_EMBEDDING_VERSION"),
    )
    logging.info("✅ Azure OpenAI embeddings initialized.")

    # Step 9: Chunk text using SemanticChunker
    st.subheader("🔹 Chunking file...")
    logging.info("🔹 Starting chunking...")
    text_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
    documents = text_splitter.create_documents([text])
    st.write(f"Chunks created: {len(documents)}")
    logging.info(f"✅ Text split into {len(documents)} chunks.")

    # Step 10: Store embeddings in ChromaDB
    st.subheader("🔹 Embedding and storing in ChromaDB...")
    persist_dir = "chroma_db"
    os.makedirs(persist_dir, exist_ok=True)

    try:
        chroma_client = chromadb.PersistentClient(path="./rag-chroma-db")
        collection = chroma_client.get_or_create_collection(name="rag_collection")
        logging.info("💾 Storing embeddings in ChromaDB...")

        for idx, doc in enumerate(documents):
            embedding = embeddings.embed_documents([doc.page_content])  # ✅ FIXED
            collection.add(
                ids=[f"doc-{idx}"],
                documents=[doc.page_content],
                embeddings=[embedding[0]]
            )
            logging.info(f"✅ Stored doc-{idx}, length: {len(doc.page_content)} characters.")

        logging.info("✅ Embeddings stored successfully.")
        st.success("✅ Embedded and stored successfully.")

        # Step 11: Allow user to query
        st.subheader("🔹 Test a question on your data")
        query = st.text_input("Ask a question:")
        if query:
            logging.info(f"🗨️ User query: {query}")
            query_embedding = embeddings.embed_query(query)
            results = collection.query(query_embeddings=[query_embedding], n_results=3)

            retrieved_docs = results["documents"][0]  # ✅ FIXED
            relevant_text, relevant_text_ids = re_rank_cross_encoders(retrieved_docs, query)

            logging.info(f"📥 Retrieved {len(retrieved_docs)} results after reranking.")
            st.write("🔍 **Top Re-ranked Results:**")
            for i, doc in enumerate(relevant_text.split("\n\n")):
                st.markdown(f"**Result {i+1}:** {doc.strip()}")

    except Exception as e:
        logging.error(f"❌ Embedding error: {str(e)}")
        st.error("❌ Embedding failed. See logs.")
