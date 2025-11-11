import os
import json
import uuid
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

from .vectorstore_base import VectorStoreBase


class CustomVectorDB(VectorStoreBase):

    def __init__(self, filepath: str):
        super().__init__()

        # CSV Path
        self.filepath = filepath
        assert self.filepath, "Filepath for CSV storage must be provided."
        assert self.filepath.endswith('.csv'), "Filepath must point to a CSV file."

        # Load existing vectors from CSV
        self.documents = self.load_vectors()

    def load_vectors(self):
        if not os.path.exists(self.filepath):
            return {}

        try:
            df = pd.read_csv(self.filepath)
            documents = {}
            
            for _, row in df.iterrows():
                doc_id = row['id']
                # Parse vector from string representation
                vector_str = row.get('vector', None)
                vector = None
                if vector_str and isinstance(vector_str, str) and vector_str != 'null':
                    # Handle vector stored as string representation
                    vector = np.fromstring(vector_str.strip('[]'), sep=',').tolist()
                
                # Parse payload JSON
                payload = {}
                if 'payload' in row and pd.notna(row['payload']):
                    try:
                        payload = json.loads(row['payload'])
                    except json.JSONDecodeError:
                        payload = {"content": str(row['payload'])}
                
                documents[doc_id] = {
                    "id": doc_id,
                    "payload": payload,
                    "vector": vector,
                }
            
            return documents

        except FileNotFoundError:
            return {}

        except Exception as e:
            print(f"Error loading vectors: {e}")
            return {}

    def _save_to_csv(self):
        """Save current documents to CSV file."""
        if not self.documents:
            return
        
        # Convert documents to DataFrame format
        rows = []
        for doc in self.documents.values():
            row = {
                'id': doc['id'],
                'payload': json.dumps(doc['payload']) if doc['payload'] else '{}',
                'vector': json.dumps(doc['vector']) if doc['vector'] else 'null',
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        df.to_csv(self.filepath, index=False)

    def add_vectors(self, vectors: List[List[float]], payloads: Optional[List[Dict[str, Any]]] = None):
        """Add vectors with metadata to the database."""
        ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
        
        if payloads is None:
            payloads = [{}] * len(vectors)
        
        if len(vectors) != len(ids) or len(vectors) != len(payloads):
            raise ValueError("Vectors, ids, and payloads must have the same length")
        
        for i, (vector, doc_id, payload) in enumerate(zip(vectors, ids, payloads)):
            # Create document following the schema
            document = {
                "id": doc_id,
                "payload": payload,
                "vector": vector,
            }
            
            self.documents[doc_id] = document
        
        # Save to CSV
        self._save_to_csv()

        return ids

    def search_vectors(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors using cosine similarity."""
        if not self.documents:
            return []
        
        query_vector = np.array(query_vector)
        results = []
        
        for doc in self.documents.values():
            if doc['vector'] is None:
                continue
                
            doc_vector = np.array(doc['vector'])
            
            # Compute cosine similarity
            dot_product = np.dot(query_vector, doc_vector)
            norm_query = np.linalg.norm(query_vector)
            norm_doc = np.linalg.norm(doc_vector)
            
            if norm_query == 0 or norm_doc == 0:
                similarity = 0
            else:
                similarity = dot_product / (norm_query * norm_doc)
            
            # Create result document with score
            result_doc = doc.copy()
            result_doc['score'] = float(similarity)
            results.append(result_doc)
        
        # Sort by score (descending) and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def delete_vectors(self, ids: List[str]):
        """Delete vectors by their IDs."""
        for doc_id in ids:
            if doc_id in self.documents:
                del self.documents[doc_id]
        
        # Save updated data to CSV
        self._save_to_csv()

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by its ID."""
        return self.documents.get(doc_id)

    def list_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents in the database."""
        return list(self.documents.values())

    def count_documents(self) -> int:
        """Get the total number of documents."""
        return len(self.documents)

    def setup(self, collection_name: str, vector_size: int):
        """Setup the custom vector database."""
        # For CSV-based storage, we don't need to create collections like in Qdrant
        # But we can validate and prepare the storage
        print(f"Setting up CustomVectorDB with collection '{collection_name}' for vectors of size {vector_size}")
        
        # Store collection metadata for validation
        self.collection_name = collection_name
        self.vector_size = vector_size
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
        # If file doesn't exist, create an empty CSV with proper headers
        if not os.path.exists(self.filepath):
            empty_df = pd.DataFrame(columns=['id', 'payload', 'vector'])
            empty_df.to_csv(self.filepath, index=False)
            print(f"Created new CSV file at {self.filepath}")
        
        print(f"CustomVectorDB setup completed for collection '{collection_name}'")
        return True
