from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import uuid
from models.Category import CatTypes
from fastapi import UploadFile


class ProductBase(BaseModel):
    product_name: str
    product_description: str
    price: float
    category: list[str]
    inventory: int

    @field_validator("inventory")
    @classmethod
    def validate_inventory(cls, inventory: int) -> int:
        if inventory <= 0:
            raise ValueError("Product inventory must be greater than zero")
        return inventory

    @field_validator("price")
    @classmethod
    def validate_price(cls, price: float) -> float:
        if price <= 0:
            raise ValueError("Product price must be greater than zero")
        return price

    @field_validator("category")
    @classmethod
    def validate_categories(cls, categories: list[str]) -> list[str]:
        valid_categories = {cat.value for cat in CatTypes}
        invalid_categories = [cat for cat in categories if cat not in valid_categories]

        if invalid_categories:
            raise ValueError(
                f"Invalid categories: {invalid_categories}. "
                f"Valid categories are: {list(valid_categories)}"
            )
        return categories

    class ConfigDict:
        arbitrary_types_allowed = True
        from_attributes = True


class ProductResponse(BaseModel):
    product_name: str
    product_id: str
    product_price: float

    class ConfigDict:
        orm_mode = True
        from_attributes = True


class ProductDelete(BaseModel):
    product_id: uuid.UUID

    class ConfigDict:
        orm_mode = True
        from_attributes = True


class ProductUpdateSerializer(ProductBase):
    product_id: uuid.UUID

    class ConfigDict:
        orm_mode = True
        from_attributes = True


class VNPayPaymentCreate(BaseModel):
    order_id: str
    amount: int
    order_desc: str
    language: Optional[str] = "vn"


class VNPayQueryRequest(BaseModel):
    order_id: str
    trans_date: str


class VNPayRefundRequest(BaseModel):
    order_id: str
    amount: int
    trans_date: str
    order_desc: str


class ProductRatingSerializer(BaseModel):
    product_id: uuid.UUID
    rating: int
    comment: Optional[str] = ""


class SearchFilter(BaseModel):
    categories: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_price: Optional[str] = None

    @field_validator("sort_price")
    @classmethod
    def validate_sort_price(cls, sort_price: Optional[str]) -> Optional[str]:
        if sort_price and sort_price not in ["asc", "desc"]:
            raise ValueError("sort_price must be either 'asc' or 'desc'")
        return sort_price


class ProductCommentResponse(BaseModel):
    user_first_name: str
    user_last_name: str
    comment: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True
