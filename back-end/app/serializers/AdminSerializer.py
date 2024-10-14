from pydantic import BaseModel
from datetime import datetime as Datetime
from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime as DateTime

class AdminGetData(BaseModel):
    timestamp : DateTime


    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class AdminCreate(BaseModel):
    first_name: str = Field(..., alias="first_name")
    last_name: str = Field(..., alias="last_name")
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
    dob: DateTime = Field(..., alias="dob")

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

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