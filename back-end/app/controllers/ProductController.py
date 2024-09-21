from sqlalchemy.orm import Session
from models.Products import Product
from serializers.ProductSerializers import *
from middlewares.token_config import *

class ProductController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all_products(self):
        return self.db.query(Product).all()


    def get_single_product(self, product_id: int):
        return self.db.query(Product).filter(Product.product_id == product_id).first()


    def create_new_product(self, product: ProductCreate, current_user):
        db_product = Product(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product


    def delete_existing_product(self, product_id: int, current_user):
        db_product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
        return db_product
