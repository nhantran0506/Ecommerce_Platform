from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime
from db_connector import Base
from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    product_name: str


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    create_at_datetime = Column(DateTime, default=datetime.now)