
class EmbeddingBaseModel:

    def __init__(self, model_name, vector_size):
        self.model_name = model_name
        self.vector_size = vector_size
        self.model = None
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError("This method should be implemented by subclasses.")
