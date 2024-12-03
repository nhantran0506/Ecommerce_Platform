from pydantic import BaseModel, field_validator
from models.Category import CatTypes

class CategoryCreate(BaseModel):
    cat_name: CatTypes
    cat_description: str

    @field_validator('cat_description')
    def validate_description(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Category description cannot be empty')
        return v.strip()