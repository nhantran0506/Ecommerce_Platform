from datetime import datetime
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, DateTime, Float
from db_connector import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ShopRating(Base):
    __tablename__ = "shop_rating"
    
    id = Column(Integer, primary_key=True, index=True)  
    shop_id = Column(Integer, ForeignKey("shop.shop_id"), nullable=False)  
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) 
    rating_stars = Column(Integer, nullable=False) 
    created_at = Column(DateTime, default=datetime.now())  

    shop = relationship("Shop", back_populates="ratings", foreign_keys=[shop_id]) 
    user = relationship("User", back_populates="shop_ratings", foreign_keys=[user_id])  
        

    


class ProductRating(Base):
    __tablename__ = "product_rating"
    
    id = Column(Integer, primary_key=True, index=True)  
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)  
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) 
    rating_stars = Column(Integer, nullable=False) 
    created_at = Column(DateTime, default=datetime.now())  

    product = relationship("Product", back_populates="ratings", foreign_keys=[product_id])  
    user = relationship("User", back_populates="product_ratings", foreign_keys=[user_id]) 
         