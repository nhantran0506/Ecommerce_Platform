from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

from models.Products import Product, ProductBase
from db_connector import db_dependency

router = APIRouter(prefix="/products", tags=["products"])


class ProductCreate(ProductBase):
    pass


@router.get("/all")
def get_products(db: db_dependency):
    return db.query(Product).all()


@router.get("/")
def get_product(db: db_dependency, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(db: db_dependency, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/")
def delete_product(db: db_dependency, product_id: int):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
