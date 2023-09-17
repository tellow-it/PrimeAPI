from typing import List, Optional

from fastapi.security import HTTPAuthorizationCredentials

from schemas.response import StatusResponse
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


@router_user.get("/", description="""
                   В поле order_by_field нужно передать поле по которому нужно сделать сортировку
                   в следующем формате:
                   \n1) порядок сортировки, если по убыванию, то перед названием поля нужно поставить "-", иначе ничего не ставить
                   \n2) поле по которому будет сортировка, вот список полей, которые которые можно передать чтобы отсортировать данные в зависимости от колонки:\n
                   Имя: name\n
                   Фамилия(по нему сортируется по умолчанию "surname"): surname\n
                   Роль: role\n
                   Дата создания: created_at\n
                   Номер телефона: telephone\n
                   """)
async def get_users(on_page: Optional[int] = 10,
                    page: Optional[int] = 0,
                    search_by_surname: Optional[str] = None,
                    order_by_field: Optional[str] = "surname",
                    token: HTTPAuthorizationCredentials = Depends(auth_schema),
                    permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    if search_by_surname is not None:
        quantity_users = await User.filter(surname__icontains=search_by_surname).all().count()
        users = await User.filter(surname__icontains=search_by_surname).all().order_by(order_by_field). \
            offset(page * on_page).limit(on_page)
    else:
        quantity_users = await User.all().count()
        users = await User.all().order_by(order_by_field).offset(page * on_page).limit(on_page)
    return {"quantity_users": quantity_users,
            "users": users}


@router_user.post("/create", response_model=UserSchema, status_code=201)
async def create_user(user: UserSchema,
                      token: HTTPAuthorizationCredentials = Depends(auth_schema),
                      permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    # password = generate_password()
    user.password = hashing_password(user.password)
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return user_obj


@router_user.get("/{user_id}", response_model=UserSchemaRead, status_code=200)
async def get_user(user_id: int,
                   token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        try:
            return await User.get(id=user_id)
        except HTTPNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with id {user_id} not found!')
    else:
        if user_info['id'] == user_id:
            try:
                return await User.get(id=user_id)
            except HTTPNotFoundError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'User with id {user_id} not found!')
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The user does not have access to the resource'
            )


@router_user.put("/update/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserSchema,
                      token: HTTPAuthorizationCredentials = Depends(auth_schema),
                      permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    try:
        await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
        return await User.get(id=user_id)
    except HTTPNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found!')


@router_user.patch("/update-password/{user_id}", response_model=UserSchema)
async def update_password_user(user_id: int,
                               user_password: UserUpdatePassword,
                               token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    try:
        user_obj = await User.get(id=user_id)
    except HTTPNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {user_id} not found!')
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
    return StatusResponse(message=f"Success delete {user_id}")
