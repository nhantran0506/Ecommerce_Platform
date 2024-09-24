from fastapi import APIRouter, status, Request, Depends
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.AISerializer import *
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from middlewares import token_config
from controllers.RecommedController import RecommendedController
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommed", tags=["recommed"])


@router.post("/get_recommed/")
async def get_recommed(recommed_controller : RecommendedController = Depends(), current_user : User = Depends(token_config.get_current_user())):
    try:
        return await recommed_controller.get_recommed(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/get_recommed/")
async def get_recommed(recommed_controller : RecommendedController = Depends()):
    try:
        return await recommed_controller.get_default_recommed()
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )