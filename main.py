import streamlit as st
from dotenv import load_dotenv

from src.vectorstore.qdrant_client import Qdrant
from src.embeddings.openai_embedder import OpenAIEmbeddingModel

assert load_dotenv(), "Failed to load .env file"


@st.cache_resource
def get_qdrant_client(collection_name: str, vector_size: int, host: str = "localhost", port: int = 6333) -> Qdrant:
    """Initialize and return a Qdrant client instance."""
    qdrant_client = Qdrant(collection_name=collection_name, vector_size=vector_size, host=host, port=port)
    return qdrant_client

@st.cache_resource
def get_openai_embedder(model_name: str = "text-embedding-3-small", vector_size: int = 1536) -> OpenAIEmbeddingModel:
    """Initialize and return an OpenAI embedding model instance."""
    embedder = OpenAIEmbeddingModel(model_name=model_name, vector_size=vector_size)
    return embedder

# Title
st.title("AI Solutions Engineer Case Study")
st.write("This is a placeholder for the main application.")

# Initialize Qdrant client (example usage)
qdrant_client = get_qdrant_client(collection_name="example_collection", vector_size=1536)
st.write(f"Host: {qdrant_client.host}, Port: {qdrant_client.port}, Collection: {qdrant_client.collection_name}")

# Initialize OpenAI embedder (example usage)
openai_embedder = get_openai_embedder(model_name="text-embedding-3-small", vector_size=1536)
st.write(f"OpenAI Embedder Model: {openai_embedder.model_name}, Vector Size: {openai_embedder.vector_size}")

