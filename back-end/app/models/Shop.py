from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid


class Shop(Base):
    __tablename__ = "shop"
    shop_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    shop_name: Mapped[String] = mapped_column(String, nullable=False)
    shop_address: Mapped[String] = mapped_column(String, nullable=False)
    shop_phone_number: Mapped[String] = mapped_column(String, nullable=False)
    shop_bio: Mapped[String] = mapped_column(String)
    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    avg_stars: Mapped[Float] = mapped_column(Float, nullable=True, default=0.0)
    total_ratings: Mapped[Integer] = mapped_column(Integer, nullable=True, default=0)

    owner: Mapped["User"] = relationship("User", back_populates="shops")
    ratings: Mapped["ShopRating"] = relationship("ShopRating", back_populates="shop")
    shop_products: Mapped["ShopProduct"] = relationship(
        "ShopProduct", back_populates="shop"
    )
