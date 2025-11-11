import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.models.document import Document


class Qdrant:

    def __init__(self, collection_name: str, vector_size: int, host: str = "localhost", port: int = 6333):
        self.collection_name = collection_name
        self.vector_size = vector_size

        self.host = host or os.getenv("QDRANT_BASE_URL", "localhost")
        self.port = port or int(os.getenv("QDRANT_PORT", 6333))
        self.client = QdrantClient(host=self.host, port=self.port)

        self.setup()

    def setup_collection(self, collection_name: str, vector_size: int):
        # Code to setup Qdrant collection
        if self.client.collection_exists(collection_name=collection_name):
            print(f"Collection {collection_name} already exists.")
            return

        created = self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

        if not created:
            raise Exception(f"Failed to create collection {collection_name}")
        
        print(f"Collection {collection_name} created successfully.")

    def setup(self):
        # Setup code for Qdrant client
        self.setup_collection(collection_name=self.collection_name, vector_size=self.vector_size)

    def get_collections(self):
        return self.client.get_collections()
    
    def search(self, query_vector: list[float], top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        return results

    def insert_document(self, document: Document) -> dict:
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            points=[document.to_point()]
        )
        print(f"Inserted document ID: {document.id} into collection: {self.collection_name}")
        print(f"Operation info: {operation_info}")
        return operation_info.model_dump()
    