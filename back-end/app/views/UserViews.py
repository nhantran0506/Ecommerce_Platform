from fastapi import APIRouter, status, Request, Depends, HTTPException
from controllers.UserController import UserController
from fastapi.responses import JSONResponse
from models.Users import User
from serializers.UserSearializers import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from middlewares import token_config
from db_connector import get_db
import logging
from fastapi.security import OAuth2PasswordRequestForm
from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    FACEBOOK_CLIENT_ID,
    FACEBOOK_REDIRECT_URI,
)
from middlewares import routing_config

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(user: UserLogin, user_controller: UserController = Depends()):
    try:
        return await user_controller.login(user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# # google login
# @router.get("/get_google_login")
# async def get_google_login(request: Request):
#     try:

#         redirect_uri = request.url_for("login_google")

#         redirect_response = (
#             await routing_config.RouteConfig.oauth.google.authorize_redirect(
#                 request,
#                 redirect_uri,
#             )
#         )
#         google_redirect_url = str(redirect_response.headers["location"])

#         return JSONResponse(content={"url": google_redirect_url})
#     except Exception as e:
#         logger.error("Error in /get_google_login: %s", str(e), exc_info=True)
#         raise HTTPException(status_code=500, detail="Error generating Google login URL")


# @router.get("/login_google")
# async def login_google(request: Request, user_controller: UserController = Depends()):
#     try:
#         # state = request.session["state"]

#         # if not state or state != request.query_params.get("state"):
#         #     raise HTTPException(status_code=400, detail="State mismatch")

#         token = await routing_config.RouteConfig.oauth.google.authorize_access_token(
#             request
#         )
#         user_informations = token.get("userinfo")
#         return await user_controller.login_google(user_informations)
#     except Exception as e:
#         logger.error(f"Error in /login_google: {str(e)}", exc_info=True)
#         return JSONResponse(
#             content={"Message": "Unexpected error"},
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# fb login
# @router.post("/get_fb_login")
# async def get_fb_login():
#     return {
#         "url": f"https://www.facebook.com/v21.0/dialog/oauth?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={FACEBOOK_REDIRECT_URI}&scope=email,public_profile&response_type=code"
#     }


# @router.get("/login_fb")
# async def login_fb(code: str, user_controller: UserController = Depends()):
#     try:
#         return await user_controller.login_fb(code)
#     except Exception as e:
#         logger.error(str(e))
#         return JSONResponse(
#             content={"Message": "Unexpected error"},
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


@router.post("/signup")
async def signup(
    user: UserCreateSerializer, user_controller: UserController = Depends()
):
    try:
        return await user_controller.signup(user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/change_password")
async def change_password(
    user_update_password: UserChangePasswordSerializer,
    user_controller: UserController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await user_controller.update_password(
            user_update_password, current_user=current_user
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/get_current_user")
async def get_current_user(
    user_controller: UserController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await user_controller.get_current_user(current_user=current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/update_user")
async def update_user(
    user_update: UserUpdate,
    user_controller: UserController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:
        return await user_controller.update_user(user_update, current_user=current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/delete_user")
async def delete_user(
    user_controller: UserController = Depends(),
    current_user=Depends(token_config.get_current_user),
):
    try:

        return await user_controller.delete_user(current_user)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/forgot_password")
async def forgot_password(
    user_data: UserForgotPassword, user_controller: UserController = Depends()
):
    try:
        return await user_controller.forgot_password(user_data)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/validate_temp_code")
async def validate_temp_code(
    user_data: UserValidateCode, user_controller: UserController = Depends()
):
    try:
        return await user_controller.validate_temp_code(user_data)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/{user_id}")
async def get_user(user_id: str, user_controller: UserController = Depends()):
    try:
        return await user_controller.get_user_by_id(user_id)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/change_password_with_code")
async def change_password_with_code(
    user_update_password: UserChangeNewPasswordSerializer,
    temp_code: str,
    user_email: str,
    user_controller: UserController = Depends(),
):
    try:
        return await user_controller.change_password_with_code(
            user_update_password, temp_code, user_email=user_email
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"Message": "Unexpected error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
