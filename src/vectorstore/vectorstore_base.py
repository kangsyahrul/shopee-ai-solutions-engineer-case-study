
class VectorStoreBase:
    """Base class for vector stores."""

    def setup(self, collection_name: str, vector_size: int):
        raise NotImplementedError("setup method not implemented.")

    def add_vectors(self, vectors, payloads=[]):
        raise NotImplementedError("add_vectors method not implemented.")

    def search_vectors(self, query_vector, top_k=5):
        raise NotImplementedError("search_vectors method not implemented.")

    def delete_vectors(self, ids):
        raise NotImplementedError("delete_vectors method not implemented.")
    