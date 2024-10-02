from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db_connector import Base
from models.CartProduct import CartProduct

class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    product_name: Mapped[String] = mapped_column(String)
    product_description: Mapped[String] = mapped_column(String)
    create_at_datetime: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    price: Mapped[Float] = mapped_column(Float)

    ratings: Mapped["ProductRating"] = relationship(
        "ProductRating", back_populates="product"
    )
    cart_products: Mapped[list["CartProduct"]] = relationship(
        "CartProduct", back_populates="product"
    )
    cat_products : Mapped["CategoryProduct"] = relationship("CategoryProduct",back_populates="product")
