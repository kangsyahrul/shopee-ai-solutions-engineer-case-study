from langchain_openai import OpenAIEmbeddings
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from .embedder_base import EmbeddingBaseModel


class OpenAIEmbeddingModel(EmbeddingBaseModel):

    def __init__(self, model_name: str = "text-embedding-3-small", vector_size: int = 1536):
        super().__init__(model_name, vector_size)

        self.model = OpenAIEmbeddings(
            model=model_name,
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
    )
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.embed_documents(texts)
        return vectors
    
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5),
    )
    def embed_query(self, query: str) -> list[float]:
        vector = self.model.embed_query(query)
        return vector
