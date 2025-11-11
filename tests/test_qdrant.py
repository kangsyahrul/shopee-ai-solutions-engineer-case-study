import os
import pytest
from dotenv import load_dotenv

assert load_dotenv(), "Failed to load .env file"

from src.vectorstore.qdrant_client import Qdrant


class TestQdrant:
    """Test suite for Qdrant vector store client."""

    def test_initialization(self):
        """Test Qdrant client initialization with default parameters."""
        # Arrange & Act
        qdrant = Qdrant()
        
        # Assert
        # assert qdrant.collection_name == "test_collection"
        # assert qdrant.vector_size == 1536
        assert qdrant.host == "localhost"
        assert qdrant.port == 6333
        assert qdrant.client is not None

