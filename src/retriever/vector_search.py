
from src.models.document import Document
from src.vectorstore.vectorstore_base import VectorStoreBase
from src.vectorstore.qdrant_client import Qdrant
from src.embeddings.openai_embedder import OpenAIEmbeddingModel


class VectorSearchRetriever:

    def __init__(self, vector_store: VectorStoreBase, embedder: OpenAIEmbeddingModel):
        self.vector_store = vector_store
        self.embedder = embedder

        self.setup()

    def setup(self):
        self.vector_store.setup(collection_name=self.collection_name, vector_size=self.embedder.vector_size)
    
    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embedder.embed_query(query)
        results = self.vector_store.search_vectors(query_vector, top_k=top_k)
        return results
    
    def add_document(self, document: Document) -> dict:
        vector = self.embedder.embed_texts([document.payload["content"]])[0]
        document.vector = vector
        result = self.vector_store.add_vectors(
            vectors=[document.vector],
            payloads=[document.payload],
        )
        return result
