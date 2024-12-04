from pydantic import BaseModel, field_validator
from models.Category import CatTypes
from datetime import datetime as DateTime

class CategoryCreate(BaseModel):
    cat_name: CatTypes
    cat_description: str

    @field_validator('cat_description')
    def validate_description(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Category description cannot be empty')
        return v.strip()

class AdminCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    dob: DateTime

    @field_validator('username')
    def validate_username(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Username cannot be empty')
        return v.strip()

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class AdminGetData(BaseModel):
    timestamp: DateTime

