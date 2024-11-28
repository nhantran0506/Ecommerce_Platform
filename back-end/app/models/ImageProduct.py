from sqlalchemy import ForeignKey, UUID, Column, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from db_connector import Base



class ImageProduct(Base):
    __tablename__ = 'image_products'

    image_url: Mapped[String] = mapped_column(String, unique=True, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('products.product_id'), primary_key=True, index=True)

    product: Mapped["Product"] = relationship("Product", back_populates="image_product")