from pydantic import BaseModel


class Document(BaseModel):
    id: str = None
    content: str
    vector: list[float]
    metadata: dict = {}

    def to_point(self) -> dict:
        return {
            "id": self.id,
            "vector": self.vector,
            "payload": {
                "content": self.content,
                **self.metadata
            }
        }
