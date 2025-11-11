import streamlit as st
from uuid import uuid4

from src.vectorstore.custom_vectordb import CustomVectorDB
from src.embeddings.openai_embedder import OpenAIEmbeddingModel
from src.models.document import Document
from src.retriever.vector_search import VectorSearchRetriever

st.sidebar.markdown("# Custom Vector Database ❄️")

file_path = "data/custom_vector_db/vectors.csv"
custom_vector_db = CustomVectorDB(file_path)

st.title("Custom Vector Database Documents")
st.write("This page demonstrates the usage of a custom vector database backed by CSV storage.")
st.divider()

# List all documents in the custom vector database
documents = custom_vector_db.list_all_documents()
st.header("Stored Documents")
st.json(documents, expanded=False)
st.divider()

# Insert data
st.header("Add New Document")
text_input = st.text_area("Enter text to embed and store in Custom Vector DB:", "Sample text for embedding.")
if st.button("Embed and Store in Custom Vector DB"):
    # Initialize OpenAI embedder
    openai_embedder = OpenAIEmbeddingModel(model_name="text-embedding-3-small", vector_size=1536)
    
    # Initialize Retriever with Custom Vector DB
    retriever = VectorSearchRetriever(vector_store=custom_vector_db, embedder=openai_embedder)
    
    operation_info = retriever.add_document(Document(id=str(uuid4()), payload={"content": text_input}, vector=[]))
    st.success("Text embedded and stored in Custom Vector DB.")
    st.json(operation_info)
st.divider()

# Query data
st.header("Search Documents")
query_input = st.text_input("Enter query text to search in Custom Vector DB:", "Sample query.")
if st.button("Search in Custom Vector DB"):
    # Initialize OpenAI embedder
    openai_embedder = OpenAIEmbeddingModel(model_name="text-embedding-3-small", vector_size=1536)
    
    # Initialize Retriever with Custom Vector DB
    retriever = VectorSearchRetriever(vector_store=custom_vector_db, embedder=openai_embedder)
    
    results = retriever.retrieve(query=query_input, top_k=5)
    st.success("Search completed.")
    st.json(results)
