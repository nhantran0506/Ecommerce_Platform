from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db_connector import Base

class Product(Base):
    __tablename__ = "products"
    product_id :Mapped[Integer] = mapped_column(Integer, primary_key=True, index=True)
    product_name :Mapped[String]= mapped_column(String)
    product_description :Mapped[String]= mapped_column(String)
    create_at_datetime:Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    price :Mapped[Integer]= mapped_column(Integer)

    ratings : Mapped["ProductRating"] = relationship("ProductRating", back_populates="product")
