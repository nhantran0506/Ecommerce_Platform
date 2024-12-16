from datetime import datetime
from sqlalchemy import (
    Boolean,
    String,
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Float,
    Enum,
)
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped


class ShopProduct(Base):
    __tablename__ = "shop_products"
    shop_id = Column(
        UUID(as_uuid=True), ForeignKey("shop.shop_id"), primary_key=True, nullable=False
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    shop: Mapped["Shop"] = relationship("Shop", back_populates="shop_products")
    product: Mapped["Product"] = relationship("Product", back_populates="shop_products")
