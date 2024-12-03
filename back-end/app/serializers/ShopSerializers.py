from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re
import uuid


class ShopBase(BaseModel):
    shop_name: str
    shop_address: str
    shop_phone_number: str
    shop_bio: str

    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True

    @field_validator("shop_phone_number")
    def validate_shop_phone_number(cls, value):
        if not re.match(r"^[0-9]{10}$", value):
            raise ValueError("Invalid phone number")

        return value


class ShopCreate(ShopBase):
    pass


class ShopRatingSerializer(BaseModel):
    shop_id: uuid.UUID
    rating: int
    comment: Optional[str] = ""


class ShopGetData(BaseModel):
    timestamp: datetime
