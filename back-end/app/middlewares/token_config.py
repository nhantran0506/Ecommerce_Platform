from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWSError, jwt
from fastapi import HTTPException, status, Depends, WebSocket
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_connector import get_db
from models.Authentication import Authentication
from models.Users import User
from config import ALGORITHM, SERECT_KEY, EXPIRE_TOKEN_TIME

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=EXPIRE_TOKEN_TIME)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SERECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SERECT_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("user_name")
        if not user_name:
            raise credentials_exception

        query = select(Authentication).where(Authentication.user_name == user_name)
        result = await db.execute(query)

        user_query = select(User).where(User.email == user_name)
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()

        if not user:
            raise credentials_exception
        return user
    except (JWSError, KeyError):
        raise credentials_exception


async def authenticate_user(db: AsyncSession, user_name: str, password: str):
    query = select(Authentication).where(Authentication.user_name == user_name)
    result = await db.execute(query)
    user_auth = result.scalar_one_or_none()

    if not user_auth or not user_auth.verify_password(password):
        return False
    return user_auth


async def get_current_user_ws(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    token = websocket.query_params.get("token")
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SERECT_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("user_name")
        if not user_name:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception

        query = select(Authentication).where(Authentication.user_name == user_name)
        result = await db.execute(query)

        user_query = select(User).where(User.email == user_name)
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()

        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        return user
    except (JWSError, KeyError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise credentials_exception
