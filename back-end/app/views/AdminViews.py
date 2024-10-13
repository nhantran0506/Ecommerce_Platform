from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import logging
from middlewares import token_config
from serializers.AdminSerializer import *
from controllers.AdminController import AdminController
from typing import List


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])



@router.post('/create_admin')
async def create_admin(admin_data : AdminCreate, admin_controller : AdminController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await admin_controller.create_admin(admin_data , current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post('/get_number_user')
async def get_number_user(admin_controller : AdminController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await admin_controller.get_number_user(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post('/get_current_revenue')
async def get_current_revenue(admin_controller : AdminController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await admin_controller.get_current_revenue(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post('/get_number_shops')
async def get_number_shops(admin_controller : AdminController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await admin_controller.get_number_shops(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )




@router.post("/get_revenue")
async def get_revenue(admin_data : AdminGetData,admin_controller : AdminController = Depends(), current_user = Depends(token_config.get_current_user)):
    try:
        return await admin_controller.get_revenue(admin_data , current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



