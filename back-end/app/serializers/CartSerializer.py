from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import UUID4

class CartModify(BaseModel):
    product_id : UUID4
    quantity : int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True



