from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime as DateTime
import re

class UserForgotPassword(BaseModel):
    email : str
    

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
    dob: DateTime = Field(..., alias="dob")

    @field_validator("email")
    def validate_email(cls, value):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid email")
        return value

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r"^[0-9]{10}$", value):
            raise ValueError("Invalid phone number")

        return value

    @field_validator("password")
    def validate_password(cls, value):
        pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*().]).+$"
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one uppercase letter, one digit, and one special character"
            )

        return value


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(..., alias="first_name")
    last_name: Optional[str] = Field(..., alias="last_name")
    address: Optional[str] = Field(..., alias="address")
    dob: Optional[DateTime] = Field(..., alias="dob")


class UserLogin(BaseModel):
    user_name: str = Field(..., alias="user_name")
    password: str = Field(..., alias="password")
