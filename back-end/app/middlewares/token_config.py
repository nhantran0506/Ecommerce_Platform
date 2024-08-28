from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWSError, jwt
from fastapi import HTTPException, status, Depends
from db_connector import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.Authentication import Authentication
from fastapi import status, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from config import ALGORITHM, SERECT_KEY, EXPIRE_TOKEN_TIME

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TOKEN_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SERECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: str):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SERECT_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("user_name", "")
        if user_name:
            user = Authentication.get_user_by_username(db, user_name)
            if user is None:
                raise credentials_exceptions
            return user
        raise "credentials_exceptions"
    except:
        raise credentials_exceptions


def authenticate_user(db: Session, user_name: str, password: str):
    user = Authentication.get_user_by_username(db, user_name)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def get_user_role(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    token = credentials.credentials  # Extract token from credentials
    user = get_current_user(db=db, token=token)
    if user:
        return user.role
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Could not determine user role"
        )
