import os
import pytest
from dotenv import load_dotenv

assert load_dotenv(), "Failed to load .env file"

from src.embeddings.openai_embedder import OpenAIEmbeddingModel
from src.embeddings.embedder_base import EmbeddingBaseModel


class TestOpenAIEmbeddingModel:

    @pytest.fixture
    def embedder(self) -> OpenAIEmbeddingModel:
        # Skip tests if no API key is available
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set - skipping real API tests")
        
        return OpenAIEmbeddingModel(model_name="text-embedding-3-small", vector_size=1536)

    def test_embed_texts(self, embedder: OpenAIEmbeddingModel):
        # Arrange
        texts = ["Hello world", "This is a test", "OpenAI embeddings"]
        
        # Act
        result = embedder.embed_texts(texts)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == len(texts)
        for embedding in result:
            assert isinstance(embedding, list)
            assert len(embedding) == embedder.vector_size
            assert all(isinstance(val, float) for val in embedding)

    def test_embed_query(self, embedder: OpenAIEmbeddingModel):
        # Arrange
        query = "What is machine learning?"
        
        # Act
        result = embedder.embed_query(query)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == embedder.vector_size
        assert all(isinstance(val, float) for val in result)

