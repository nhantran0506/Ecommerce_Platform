from pydantic import BaseModel
from datetime import datetime as Datetime
from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime as DateTime

class AdminGetData(BaseModel):
    timestamp : DateTime


    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True


class AdminCreate(BaseModel):
    first_name: str = Field(..., alias="first_name")
    last_name: str = Field(..., alias="last_name")
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
    dob: DateTime = Field(..., alias="dob")

    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True

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