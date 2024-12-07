from fastapi import APIRouter, status, Depends, File, Form, UploadFile, Request, Query
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.ProductSerializers import *
from controllers.ProductController import ProductController
from controllers.EmbeddingController import EmbeddingController
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional, List


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["products"])


@router.get("/all")
async def get_products(product_controller: ProductController = Depends()):
    try:
        return await product_controller.get_all_products()
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/create")
async def create_product(
    product_name: str = Form(...),
    product_description: str = Form(...),
    price: float = Form(...),
    category: list[str] = Form(...),
    inventory : int = Form(...),
    images: list[UploadFile] = File(...),
    current_user=Depends(token_config.get_current_user),
    product_controller: ProductController = Depends(),
):
    try:
        product = ProductBase(
            product_name=product_name,
            product_description=product_description,
            price=price,
            category=category,
            inventory = inventory,
        )
        return await product_controller.create_product(
            product=product, image_list=images, current_user=current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/product_update")
async def product_update(
    product_name: str = Form(...),
    product_id: uuid.UUID = Form(...),
    product_description: str = Form(...),
    price: float = Form(...),
    inventory : int = Form(...),
    category: list[str] = Form(...),
    images: Optional[list[UploadFile]] = File(...),
    product_controller: ProductController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        product = ProductUpdateSerializer(
            product_id=product_id,
            product_name=product_name,
            product_description=product_description,
            price=price,
            inventory = inventory,
            category=category,
        )

        return await product_controller.update_product(
            product_update=product, image_list=images, current_user=current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/search_products")
async def search_products(
    user_query: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_price: Optional[str] = Query(None, description="'asc' for low to high, 'desc' for high to low"),
    embedding_controller: EmbeddingController = Depends(),
):
    filters = SearchFilter(
        categories=categories, 
        min_price=min_price, 
        max_price=max_price,
        sort_price=sort_price
    )
    return await embedding_controller.search_product(user_query, filters)


@router.post("/get_all_products_shop")
async def get_all_products_shop(
    product_controller: ProductController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await product_controller.get_all_products_shop(current_user=current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/product_rating")
async def product_rating(
    product_rating: ProductRatingSerializer,
    product_controller: ProductController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await product_controller.product_rating(product_rating, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/{product_id}")
async def product_delete(
    product_id: uuid.UUID,
    product_controller: ProductController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await product_controller.delete_product(
            product_id=product_id, current_user=current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/get_all_products_cat")
async def get_all_products_cat(product_controller: ProductController = Depends()):
    try:
        return await product_controller.get_all_products_cat()
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/{product_id}")
async def get_product(
    product_id: uuid.UUID,
    product_controller: ProductController = Depends(),
    current_user = Depends(token_config.get_current_user)
):
    try:
        return await product_controller.post_single_product(
            product_id=product_id, current_user = current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{product_id}")
async def get_product(
    product_id: uuid.UUID,
    product_controller: ProductController = Depends(),
):
    try:
        return await product_controller.get_single_product(
            product_id=product_id
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{product_id}/comments")
async def get_product_comments(
    product_id: uuid.UUID, product_controller: ProductController = Depends()
):
    try:
        return await product_controller.get_product_comments(product_id)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
