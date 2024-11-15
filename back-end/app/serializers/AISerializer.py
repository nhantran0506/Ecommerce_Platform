from pydantic import BaseModel


class EmbeddingPayload(BaseModel):
    model : str
    url : str


class QueryPayload(BaseModel):
    model : str
    session_id : str
    query : str
    current_route : str
    
    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True