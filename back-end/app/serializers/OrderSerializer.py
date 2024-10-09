from pydantic import BaseModel
import uuid

class OderItems(BaseModel):
    product_id : uuid.UUID
    quantity : int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True