from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid


class ShopRating(Base):
    __tablename__ = "shop_rating"

    shop_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("shop.shop_id"), nullable=False, primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        primary_key=True,
    )
    rating_stars: Mapped[Integer] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    comment: Mapped[String] = mapped_column(String, nullable=True)

    shop: Mapped["Shop"] = relationship("Shop", back_populates="ratings")
    user: Mapped["User"] = relationship("User", back_populates="shop_ratings")


class ProductRating(Base):
    __tablename__ = "product_rating"

    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.product_id"),
        nullable=False,
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        primary_key=True,
    )
    rating_stars: Mapped[Integer] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    comment: Mapped[String] = mapped_column(String, nullable=True)

    product: Mapped["Product"] = relationship("Product", back_populates="ratings")
    user: Mapped["User"] = relationship("User", back_populates="product_ratings")
