from sqlalchemy import (
    ForeignKey,
    UUID,
    Column,
    String,
    ForeignKey,
    Boolean,
    Integer,
    DateTime,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from datetime import datetime
from db_connector import Base


class Cart(Base):
    __tablename__ = "cart"
    cart_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )

    cart_products: Mapped["CartProduct"] = relationship(
        "CartProduct", back_populates="cart"
    )
