from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re
import uuid


class ShopBase(BaseModel):
    shop_name: str
    shop_address: str
    shop_bio: str

    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True



class ShopCreate(ShopBase):
    pass


class ShopRatingSerializer(BaseModel):
    shop_id: uuid.UUID
    rating: int
    comment: Optional[str] = ""


class ShopGetData(BaseModel):
    timestamp: datetime
