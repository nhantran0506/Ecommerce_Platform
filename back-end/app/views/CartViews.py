from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.CartSerializer import *
from controllers.CartController import CartController
from typing import List
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/add_products")
async def add_products(product_add : CartModify,cart_controller : CartController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await cart_controller.add_product(product_add, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/update_products")
async def add_products(product_list : List[CartModify],cart_controller : CartController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await cart_controller.update_cart(product_list, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )