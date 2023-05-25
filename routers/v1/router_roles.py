from typing import List

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from database.models.role import Roles

router_role = APIRouter(prefix="/role", tags=["Roles"])


@router_role.get("/")
async def get_roles(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return {"roles": {"admin": Roles.admin.name,
                      "user": Roles.user.name,
                      "advanced_user": Roles.advanced_user.name}}

# @router_role.post("/create", response_model=RoleSchema, status_code=201)
# async def create_role(role: RoleSchemaCreate):
#     role_obj = await Role.create(**role.dict(exclude_unset=True))
#     return await RoleSchema.from_tortoise_orm(role_obj)
#
#
# @router_role.get("/{role_id}", response_model=RoleSchema,
#                  responses={404: {"model": HTTPNotFoundError}}, status_code=200)
# async def get_role(role_id: int):
#     return await RoleSchema.from_queryset_single(Role.get(id=role_id))
#
#
# @router_role.put(
#     "/update/{role_id}", response_model=RoleSchema, responses={404: {"model": HTTPNotFoundError}}
# )
# async def update_role(role_id: int, role: RoleSchemaUpdate):
#     await Role.filter(id=role_id).update(**role.dict(exclude_unset=True))
#     return await RoleSchema.from_queryset_single(Role.get(id=role_id))
#
#
# @router_role.delete("/delete/{role_id}", responses={404: {"model": HTTPNotFoundError}})
# async def delete_role(role_id: int):
#     deleted_count = await Role.filter(id=role_id).delete()
#     if not deleted_count:
#         raise HTTPException(status_code=404, detail=f"Role {role_id} not found")
#     return Status(message=f"Success delete {role_id}")
