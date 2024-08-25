from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime as DateTime

class UserGetSerializer(BaseModel):
    first_name: str
    last_name: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class UserPostSerializer(UserGetSerializer):
    address: Optional[str] = None
    dob: Optional[DateTime] = None
    email: Optional[str] = None

class UserCreateSerializer(UserPostSerializer):
    first_name: str = Field(..., alias="first_name")
    last_name: str = Field(..., alias="last_name")
    phone_number: str = Field(..., alias="phone_number")
    password: str = Field(..., alias="password")
    address: str = Field(..., alias="address")
    email: str = Field(..., alias="email")
    dob: Optional[DateTime] = Field(..., alias="dob")


class UserLogin(BaseModel):
    user_name: str = Field(..., alias="user_name")
    password: str = Field(..., alias="password")