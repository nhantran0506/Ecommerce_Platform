from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db_connector import Base

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    product_description = Column(String)
    create_at_datetime = Column(DateTime, default=datetime.now)
    price = Column(Integer)

    ratings = relationship("ProductRating", back_populates="product")
