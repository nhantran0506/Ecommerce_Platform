from sqlalchemy import (
    Boolean,
    String,
    Column,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
import enum
from db_connector import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from models.Ratings import *
import uuid


class CategoryProduct(Base):
    __tablename__ = "category_products"

    cat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('categories.cat_id'), primary_key=True)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('products.product_id'), primary_key=True)

    product : Mapped["Product"] = relationship("Product",back_populates="cat_products")
    category : Mapped["Category"] = relationship("Category",back_populates="cat_products")

    