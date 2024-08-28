from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from db_connector import get_db
from models.Products import Product, ProductBase

router = APIRouter(prefix="/products", tags=["products"])


class ProductCreate(ProductBase):
    pass


@router.get("/all")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/")
def get_product(product_id: int , db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.product_id == product_id).first()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate , db: Session = Depends(get_db) ):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
