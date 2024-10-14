from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.OrderSerializer import *
from controllers.OrderController import OrderController
from typing import List
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/order", tags=["order"])



@router.get("/get_order_details")
async def get_order_details(order_items : List[OderItems], order_controller : OrderController = Depends()):
    try:
        return await order_controller.get_order_details(order_items)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/order_products")
async def order_products(order_items : List[OderItems], order_controller : OrderController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await order_controller.order_product(order_items, current_user)
    except Exception as e:
        logger.error(str(e))

        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )