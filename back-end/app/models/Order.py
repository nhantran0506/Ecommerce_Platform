from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid


class Order(Base):
    __tablename__ = "orders"
    order_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    created_at : Mapped[UUID] = mapped_column(DateTime, nullable=False, default=datetime.now)

    order_items : Mapped["OrderItem"] = relationship("OrderItem", back_populates="order")
