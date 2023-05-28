from typing import List, Optional

from fastapi.security import HTTPAuthorizationCredentials

from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from utils.generate_password import generate_password
from utils.hash_password import hashing_password, verify_password
from schemas.user import UserSchema, UserSchemaRead, UserUpdatePassword
from database.models.user import User
from routers.v1.router_auth import auth_schema
from utils.jwt import decode_access_token
from utils.permission import PermissionChecker

router_user = APIRouter(prefix="/user", tags=["Users"])


@router_user.get("/", response_model=List[UserSchemaRead])
async def get_users(on_page: Optional[int] = 0,
                    page: Optional[int] = 0,
                    token: HTTPAuthorizationCredentials = Depends(auth_schema),
                    permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    return await User.all().offset(page * on_page).limit(on_page)


@router_user.post("/create", response_model=UserSchema, status_code=201)
async def create_user(user: UserSchema,
                      token: HTTPAuthorizationCredentials = Depends(auth_schema),
                      permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    # password = generate_password()
    user.password = hashing_password(user.password)
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return user_obj


@router_user.get("/{user_id}", response_model=UserSchemaRead,
                 responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_user(user_id: int,
                   token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        return await User.get(id=user_id)
    else:
        if user_info['id'] == user_id:
            return await User.get(id=user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The user does not have access to the resource'
            )


@router_user.put("/update/{user_id}", response_model=UserSchema, responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, user: UserSchema,
                      token: HTTPAuthorizationCredentials = Depends(auth_schema),
                      permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User.get(id=user_id)


@router_user.patch("/update-password/{user_id}", response_model=UserSchema,
                   responses={404: {"model": HTTPNotFoundError}})
async def update_password_user(user_id: int,
                               user_password: UserUpdatePassword,
                               token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    user_obj = await User.get(id=user_id)
    if verify_password(user_password.password, user_obj.password):
        # password = generate_password()
        hashing_new_password = hashing_password(user_password.new_password)
        await user_obj.update_from_dict({'password': hashing_new_password}).save()
        return user_obj
    else:
        raise HTTPException(status_code=401, detail=f"No correct password")


@router_user.delete("/delete/{user_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int,
                      token: HTTPAuthorizationCredentials = Depends(auth_schema),
                      permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Success delete {user_id}")
