from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ShopBase(BaseModel):
    shop_name: str
    shop_address: str
    shop_phone_number: str
    shop_bio: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

class ShopCreate(ShopBase):
    pass

