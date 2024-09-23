from pydantic import BaseModel


class EmbeddingPayload(BaseModel):
    model_name : str
    url : str