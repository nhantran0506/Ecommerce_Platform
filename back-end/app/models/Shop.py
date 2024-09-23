from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Shop(Base):
    __tablename__ = "shop"
    shop_id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=False)
    shop_address = Column(String, nullable=False)
    shop_phone_number = Column(String, nullable=False)
    shop_bio = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="shops")
    ratings = relationship("ShopRating", back_populates="shop")

