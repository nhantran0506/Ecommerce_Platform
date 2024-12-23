from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db_connector import Base
from models.CartProduct import CartProduct
from models.OrderItem import *
from models.ImageProduct import ImageProduct


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    product_name: Mapped[String] = mapped_column(String)
    product_description: Mapped[String] = mapped_column(String)
    create_at_datetime: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    price: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)
    avg_stars: Mapped[Float] = mapped_column(Float, nullable=True, default=0.0)
    total_ratings: Mapped[Integer] = mapped_column(Integer, nullable=True, default=0)
    total_sales: Mapped[Integer] = mapped_column(Integer, nullable=True, default=0)
    inventory: Mapped[Integer] = mapped_column(Integer, nullable=True, default=0)

    ratings: Mapped["ProductRating"] = relationship(
        "ProductRating", back_populates="product"
    )
    cart_products: Mapped[list["CartProduct"]] = relationship(
        "CartProduct", back_populates="product"
    )
    cat_products: Mapped["CategoryProduct"] = relationship(
        "CategoryProduct", back_populates="product", cascade="all, delete-orphan"
    )
    order_items: Mapped["OrderItem"] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )
    interest: Mapped["UserInterest"] = relationship(
        "UserInterest", back_populates="product", cascade="all, delete-orphan"
    )
    shop_products: Mapped["ShopProduct"] = relationship(
        "ShopProduct", back_populates="product", cascade="all, delete-orphan"
    )

    image_product: Mapped["ImageProduct"] = relationship(
        "ImageProduct", back_populates="product", cascade="all, delete-orphan"
    )
