from typing import List
from schemas.response import Status
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from utils.generate_password import generate_password
from schemas.user import UserSchema, UserSchemaUpdate, UserSchemaCreate
from database.models.user import User

router_user = APIRouter(prefix="/user", tags=["Users"])


@router_user.get("/", response_model=List[UserSchema])
async def get_users():
    return await User.all()


@router_user.post("/create", response_model=UserSchema, status_code=201)
async def create_user(user: UserSchemaCreate):
    password = generate_password()
    user.password = password
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await user_obj


@router_user.get("/{user_id}", response_model=UserSchema,
                 responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_user(user_id: int):
    return await User.get(id=user_id)


@router_user.put("/update/{user_id}", response_model=UserSchema, responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, system: UserSchemaUpdate):
    await User.filter(id=user_id).update(**system.dict(exclude_unset=True))
    return await User.get(id=user_id)


@router_user.delete("/delete/{user_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Success delete {user_id}")
