from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class CartModify(BaseModel):
    product_id : uuid.UUID
    quantity : int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True



