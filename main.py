import streamlit as st
from dotenv import load_dotenv

from src.vectorstore.qdrant_client import Qdrant
from src.retriever.vector_search import VectorSearchRetriever
from src.embeddings.openai_embedder import OpenAIEmbeddingModel

assert load_dotenv(), "Failed to load .env file"


# @st.cache_resource
def get_qdrant_client(host: str = "localhost", port: int = 6333) -> Qdrant:
    """Initialize and return a Qdrant client instance."""
    qdrant_client = Qdrant(host=host, port=port)
    return qdrant_client

# @st.cache_resource
def get_openai_embedder(model_name: str = "text-embedding-3-small", vector_size: int = 1536) -> OpenAIEmbeddingModel:
    """Initialize and return an OpenAI embedding model instance."""
    embedder = OpenAIEmbeddingModel(model_name=model_name, vector_size=vector_size)
    return embedder

# Title
st.title("AI Solutions Engineer Case Study")
st.write("This is a placeholder for the main application.")

collection_name = "example_collection"

# Initialize Qdrant client
qdrant_client = get_qdrant_client()

# Initialize OpenAI embedder
openai_embedder = get_openai_embedder(model_name="text-embedding-3-small", vector_size=1536)
st.write(f"OpenAI Embedder Model: {openai_embedder.model_name}, Vector Size: {openai_embedder.vector_size}")

# Initialize Retriever
retriever = VectorSearchRetriever(collection_name, vector_store=qdrant_client, embedder=openai_embedder)
st.write(f"Host: {retriever.vector_store.host}, Port: {retriever.vector_store.port}, Collection: {retriever.collection_name}")
