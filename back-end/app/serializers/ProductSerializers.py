from pydantic import BaseModel, Field,field_validator
from datetime import datetime
from typing import Optional
# from models.Category import CatTypes

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    create_at_datetime: Optional[datetime] = Field(default_factory=datetime.now)
    price: int
    category : list[str]

    # @field_validator("category", each_item=True)
    # def validate_category(cls, value):
    #     if value not in [cat_type.value for cat_type in CatTypes]:
    #         raise ValueError(f"Invalid category: {value}. Must be one of {[cat_type.value for cat_type in CatTypes]}")
        # return value

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
    