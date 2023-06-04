from fastapi import APIRouter, HTTPException, Depends
from jose import jwt

from database.models.user import User
from schemas.auth import LoginSchema, TokenSchema
from utils.hash_password import verify_password
from utils.jwt import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_schema = HTTPBearer()

router_auth = APIRouter(prefix="/auth", tags=["Authorization"])


@router_auth.post("/login", status_code=200, response_model=TokenSchema)
async def login(login_data: LoginSchema):
    user_obj = await User.get_or_none(telephone=login_data.telephone)
    if user_obj:
        if verify_password(login_data.password, user_obj.password):
            user_data = {"id": user_obj.id,
                         "role": user_obj.role}
            access_token = create_access_token(user=user_data)
            refresh_token = create_refresh_token(user=user_data)
            token_type = "Bearer"
            return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type=token_type)
        else:
            raise HTTPException(status_code=401, detail="No correct password!")
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist!")


@router_auth.post("/user_data_by_token", status_code=200)
async def get_data_by_token(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return decode_access_token(token)


@router_auth.post("/refresh", status_code=200)
async def get_new_access_token(refresh_token: HTTPAuthorizationCredentials):
    token_data = decode_refresh_token(token=refresh_token)
    return create_access_token(token_data)
