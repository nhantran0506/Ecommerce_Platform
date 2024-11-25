from pydantic import BaseModel, Field,field_validator
from datetime import datetime
from typing import Optional
import uuid

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    price: float
    category : list[str]


    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True

class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    product_name : str
    product_id : str
    product_price : float
    

    class ConfigDict:
        orm_mode = True 
        from_attributes=True


class ProductDelete(BaseModel):
    product_id : uuid.UUID

    class ConfigDict:
        orm_mode = True 
        from_attributes=True

class ProductUpdateSerializer(ProductBase):
    product_id : uuid.UUID
    
    class ConfigDict:
        orm_mode = True 
        from_attributes=True