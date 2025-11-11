import os
import pandas as pd
from src.vectorstore.custom_vectordb import CustomVectorDB

class TestCustomVectorDB:
    
    def test_initialization(self):
        filepath = "data/custom_vector_db/test/test_vectors.csv"
        vectordb = CustomVectorDB(filepath=filepath)
        assert vectordb.filepath == filepath
        assert isinstance(vectordb.documents, dict)

    def test_load_vectors_empty(self, tmp_path):
        filepath = "data/custom_vector_db/test/test_vectors.csv"
        vectordb = CustomVectorDB(filepath=str(filepath))
        assert vectordb.documents == {}

    def test_load_vectors_with_data(self, tmp_path):
        data = {
            "id": ["doc1", "doc2"],
            "vector": ["[0.1, 0.2, 0.3]", "[0.4, 0.5, 0.6]"],
            "payload": ['{"content": "Document 1"}', '{"content": "Document 2"}']
        }
        df = pd.DataFrame(data)
        filepath = "data/custom_vector_db/test/vectors.csv"
        filedir = os.path.dirname(filepath)
        os.makedirs(filedir, exist_ok=True)
        df.to_csv(filepath, index=False)

        vectordb = CustomVectorDB(filepath=str(filepath))
        assert len(vectordb.documents) == 2
        assert vectordb.documents["doc1"]["vector"] == [0.1, 0.2, 0.3]
        assert vectordb.documents["doc1"]["payload"] == {"content": "Document 1"}