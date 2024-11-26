from pydantic import BaseModel, Field,field_validator
from datetime import datetime
from typing import Optional
import uuid
from models.Category import CatTypes
from fastapi import UploadFile

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    price: float
    category: list[str]
    

    @field_validator('category')
    @classmethod
    def validate_categories(cls, categories: list[str]) -> list[str]:
        valid_categories = {cat.value for cat in CatTypes}
        invalid_categories = [cat for cat in categories if cat not in valid_categories]
        
        if invalid_categories:
            raise ValueError(
                f"Invalid categories: {invalid_categories}. "
                f"Valid categories are: {list(valid_categories)}"
            )
        return categories

    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True



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