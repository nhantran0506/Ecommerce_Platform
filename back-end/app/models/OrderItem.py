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
import uuid
import enum
from datetime import datetime
from models.Order import Order


class OrderStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    TRANSPORTING = "TRANSPORTING"
    PRODUCT_ACCEPTED = "PRODUCT_ACCEPTED"
    PRODUCT_PREPARING = "PRODUCT_PREPARING"


class OrderItem(Base):
    __tablename__ = "order_items"
    order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.order_id"), primary_key=True, index=True
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.product_id"), primary_key=True
    )
    quantity: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PROCESSING
    )
    order_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    modify_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    recieved_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
