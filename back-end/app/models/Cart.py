from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from datetime import datetime
from db_connector import Base

class Cart(Base):
    __tablename__ = 'cart'
    cart_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"),nullable=False)
    created_at : Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.now())

    cart_products : Mapped[list["CartProduct"]] = relationship("CartProduct", back_populates="cart")

    def add_product(self, product: "Product", quantity: int = 1):
        cart_product = CartProduct(cart=self, product=product, quantity=quantity)
        self.cart_products.append(cart_product)



    