from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx
from fastapi import Depends, HTTPException, status
import requests
from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    FACEBOOK_CLIENT_ID,
    FACEBOOK_CLIENT_SECRET,
    FACEBOOK_REDIRECT_URI,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import httpx


async def verify_google_oauth_token(code: str) -> dict:
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    # Exchange the code for an access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)

        # Handle errors during token exchange
        if token_response.status_code != 200:
            raise ValueError("Failed to obtain access token from Google")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Access token is missing in the response")

        # Use the access token to fetch user information
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # Handle errors when fetching user info
        if user_info_response.status_code != 200:
            raise ValueError("Failed to fetch user info from Google")

        user_info = user_info_response.json()
        return user_info


async def verify_fb_oauth_token(code: str) -> dict:
    token_url = "https://graph.facebook.com/v21.0/oauth/access_token"
    user_info_url = "https://graph.facebook.com/v21.0/me"

    data = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_CLIENT_SECRET,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.get(token_url, params=data)

        if token_response.status_code != 200:
            raise ValueError("Failed to obtain access token from Facebook")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Access token is missing in the response")

        user_info_response = await client.get(
            user_info_url,
            params={"access_token": access_token, "fields": "id,name,email"},
        )

        if user_info_response.status_code != 200:
            raise ValueError("Failed to fetch user info from Facebook")

        user_info = user_info_response.json()
        return user_info
