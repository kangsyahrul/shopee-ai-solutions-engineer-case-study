import os
import uuid
from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from .vectorstore_base import VectorStoreBase


class Qdrant(VectorStoreBase):

    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "default_collection", vector_size: int = 1536):
        self.host = host or os.getenv("QDRANT_BASE_URL", "localhost")
        self.port = port or int(os.getenv("QDRANT_PORT", 6333))
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(host=self.host, port=self.port)

    def setup_collection(self, collection_name: str, vector_size: int):
        # Qdrant collection
        if self.client.collection_exists(collection_name=collection_name):
            print(f"Collection {collection_name} already exists.")

            # TODO: Ensure vector size matches
            return

        created = self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

        if not created:
            raise Exception(f"Failed to create collection {collection_name}")
        
        print(f"Collection {collection_name} created successfully.")

    def setup(self):
        # Setup collection
        self.setup_collection(collection_name=self.collection_name, vector_size=self.vector_size)

    def get_collections(self):
        return self.client.get_collections()
    
    def add_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]] = None):
        if payloads is None:
            payloads = [{}] * len(vectors)
        
        if len(vectors) != len(payloads):
            raise ValueError("Vectors and payloads must have the same length")
        
        points = []
        for i, (vector, payload) in enumerate(zip(vectors, payloads)):
            point_id = str(uuid.uuid4())
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
            points.append(point)
        
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        print(f"Added {len(points)} vectors to collection: {self.collection_name}")
        return operation_info.model_dump()

    def search_vectors(self, query_vector: List[float], top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        return results

    def delete_vectors(self, ids: List[str]):
        operation_info = self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids
        )
        
        print(f"Deleted {len(ids)} vectors from collection: {self.collection_name}")
        return operation_info
    