from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    create_at_datetime: Optional[datetime] = Field(default_factory=datetime.now)
    price: int

    class Config:
        arbitrary_types_allowed = True

class ProductCreate(ProductBase):
    pass

