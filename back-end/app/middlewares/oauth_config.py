from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx
from fastapi import Depends, HTTPException, status
from config import GOOGLE_CLIENT_ID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_google_oauth_token(token: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google OAuth token",
            )
        
        id_info = response.json()
        
        if id_info["aud"] != GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid audience in token",
            )
        
        return id_info

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
        )
