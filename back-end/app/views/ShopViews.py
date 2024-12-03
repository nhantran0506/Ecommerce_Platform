from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.ShopSerializers import *
from controllers.ShopController import ShopController

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/shops", tags=["shops"])


@router.get("/all")
async def get_shops(shop_controller: ShopController = Depends()):
    try:
        return await shop_controller.get_all_shop()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{shop_id}")
async def get_shop(shop_id: int, shop_controller: ShopController = Depends()):
    try:
        return await shop_controller.get_single_shop(shop_id=shop_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/create_shop", status_code=status.HTTP_201_CREATED)
async def create_shop(
    shop: ShopCreate,
    current_user=Depends(token_config.get_current_user),
    shop_controller: ShopController = Depends(),
):
    try:
        return await shop_controller.create_new_shop(
            shop=shop, current_user=current_user
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/delete_shop")
def delete_shop(
    shop_id: int,
    current_user=Depends(token_config.get_current_user),
    shop_controller: ShopController = Depends(),
):
    try:
        return shop_controller.delete_existing_shop(
            shop_id=shop_id, current_user=current_user
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/shop_rating")
async def shop_rating(
    shop_rating: ShopRatingSerializer,
    shop_controller: ShopController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await shop_controller.shop_rating(shop_rating, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"error": "Failing to rate shop"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/statistics/revenue")
async def shop_statistics_revenue(
    shop_data: ShopGetData,
    shop_controller: ShopController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await shop_controller.statistics_revenue(shop_data, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/statistics/top_products")
async def shop_statistics_top_products(
    shop_data: ShopGetData,
    shop_controller: ShopController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await shop_controller.statistics_top_products(shop_data, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.post("/statistics/categories")
async def shop_statistics_categories(
    shop_data: ShopGetData,
    shop_controller: ShopController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await shop_controller.statistics_categories(shop_data, current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
