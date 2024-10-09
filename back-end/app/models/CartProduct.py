from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from datetime import datetime
from db_connector import Base
from models.Cart import Cart

class CartProduct(Base):
    __tablename__ = 'cart_product'

    cart_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('cart.cart_id'), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('products.product_id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_products")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_products")