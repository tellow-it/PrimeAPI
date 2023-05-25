from jose import jwt
from database.models.user import User
from core.config import settings
from datetime import timedelta, datetime


def create_access_token(user: User):
    claims = {
        "role": user.role,
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=60 * 2)
    }
    return jwt.encode(claims=claims, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str):
    claims = jwt.decode(token.credentials, key=settings.JWT_SECRET_KEY, algorithms='HS256')
    return claims
