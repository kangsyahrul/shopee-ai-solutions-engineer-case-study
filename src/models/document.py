from pydantic import BaseModel


class Document(BaseModel):

    id: str = None
    payload: dict = {}
    vector: list[float]

    def to_point(self) -> dict:
        return {
            "id": self.id,
            "vector": self.vector,
            "payload": self.payload,
        }
