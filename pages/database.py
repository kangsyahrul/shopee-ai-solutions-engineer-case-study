import streamlit as st
from uuid import uuid4

from src.vectorstore.qdrant_client import Qdrant
from src.embeddings.openai_embedder import OpenAIEmbeddingModel
from src.models.document import Document

st.sidebar.markdown("# Vector Database ❄️")

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

st.title("Vector Database Management")
st.write("Manage your Qdrant vector database and OpenAI embeddings here.")

# Initialize Qdrant client (example usage)
qdrant_client = get_qdrant_client(collection_name="example_collection", vector_size=1536)
st.write(f"Host: {qdrant_client.host}, Port: {qdrant_client.port}, Collection: {qdrant_client.collection_name}")

# Initialize OpenAI embedder (example usage)
openai_embedder = get_openai_embedder(model_name="text-embedding-3-small", vector_size=1536)

# Insert data
text_input = st.text_area("Enter text to embed and store in Qdrant:", "Sample text for embedding.")
if st.button("Embed and Store"):
    vector = openai_embedder.embed_texts([text_input])[0]
    document = Document(id=str(uuid4()), content=text_input, vector=vector)

    qdrant_client.insert_document(document)
    st.success("Text embedded and stored in Qdrant.")

