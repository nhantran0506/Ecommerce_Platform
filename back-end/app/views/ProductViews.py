from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.ProductSerializers import *
from controllers.ProductController import ProductController
from controllers.EmbeddingController import EmbeddingController
import uuid

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
    product: ProductBase,
    current_user=Depends(token_config.get_current_user),
    product_controller: ProductController = Depends(),
):
    try:
        return await product_controller.create_product(
            product=product, current_user=current_user
        )
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
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await product_controller.get_single_product(
            product_id=product_id, current_user=current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/search_products")
async def product_search(
    user_query: str, embedding_controller: EmbeddingController = Depends()
):
    try:
        return await embedding_controller.search_product(user_query)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.route("/product_update")
async def product_update(product_update : ProductUpdateSerializer, product_controller: ProductController = Depends(),
    current_user=Depends(token_config.get_current_user)):
    try:
        return await product_controller.update_product(
            product=product_update, current_user=current_user
        )
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

