from fastapi import APIRouter, HTTPException, Depends
from database.models.user import User
from schemas.auth import LoginSchema, TokenSchema
from utils.hash_password import verify_password
from utils.jwt import create_access_token, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_schema = HTTPBearer()

router_auth = APIRouter(prefix="/auth", tags=["Authorization"])


@router_auth.post("/login", status_code=200, response_model=TokenSchema)
async def login(login_data: LoginSchema):
    user_obj = await User.get_or_none(telephone=login_data.telephone)
    if user_obj:
        if verify_password(login_data.password, user_obj.password):
            access_token = create_access_token(user=user_obj)
            token_type = "Bearer"
            return TokenSchema(access_token=access_token, token_type=token_type)
        else:
            raise HTTPException(status_code=401, detail="No correct password!")
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist!")


@router_auth.post("/user_data_by_token", status_code=200)
async def get_data_by_token(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return decode_access_token(token)
