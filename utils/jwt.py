from typing import Dict

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from database.models.user import User
from core.config import settings
from datetime import timedelta, datetime


def create_access_token(user: Dict):
    claims = {
        "role": user["role"],
        "id": user["id"],
        "exp": datetime.utcnow() + timedelta(minutes=60 * 2)
    }
    return jwt.encode(claims=claims, key=settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user: Dict):
    claims = {
        "role": user["role"],
        "id": user["id"],
        "exp": datetime.utcnow() + timedelta(minutes=60 * 24 * 7)
    }
    return jwt.encode(claims=claims, key=settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: HTTPAuthorizationCredentials):
    try:
        claims = jwt.decode(token.credentials, key=settings.JWT_ACCESS_SECRET_KEY, algorithms='HS256')
        return claims
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access token is expired')


def decode_refresh_token(token: HTTPAuthorizationCredentials):
    try:
        claims = jwt.decode(token.credentials, key=settings.JWT_REFRESH_SECRET_KEY, algorithms='HS256')
        return claims
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Refresh token is expired')
