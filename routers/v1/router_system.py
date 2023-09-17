from typing import List, Optional
from fastapi.security import HTTPAuthorizationCredentials
from routers.v1.router_auth import auth_schema
from schemas.response import StatusResponse
from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.system import SystemSchema, SystemSchemaCreate, SystemSchemaUpdate
from database.models.system import System
from utils.permission import PermissionChecker

router_system = APIRouter(prefix="/system", tags=["Systems"])


@router_system.get("/", response_model=List[SystemSchema],
                   description="""
                   В поле order_by_field нужно передать поле по которому нужно сделать сортировку
                   в следующем формате:
                   \n1) порядок сортировки, если по убыванию, то перед названием поля нужно поставить "-", иначе ничего не ставить
                   \n2) поле по которому будет сортировка, вот список полей, которые которые можно передать чтобы отсортировать данные в зависимости от колонки:\n
                   Название системы(по нему сортируется по умолчанию "system_name"): system_name\n
                   """)
async def get_systems(order_by_field: Optional[str] = "system_name",
                      token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await SystemSchema.from_queryset(System.all().order_by(order_by_field))


@router_system.post("/create", response_model=SystemSchema, status_code=201)
async def create_system(system: SystemSchemaCreate,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    system_obj = await System.create(**system.dict(exclude_unset=True))
    return await SystemSchema.from_tortoise_orm(system_obj)


@router_system.get("/{system_id}", response_model=SystemSchema, status_code=200)
async def get_system(system_id: int, token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    try:
        return await SystemSchema.from_queryset_single(System.get(id=system_id))
    except HTTPNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'System with id {system_id} not found!')


@router_system.put("/update/{system_id}", response_model=SystemSchema,)
async def update_system(system_id: int, system: SystemSchemaUpdate,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    try:
        await System.filter(id=system_id).update(**system.dict(exclude_unset=True))
        return await SystemSchema.from_queryset_single(System.get(id=system_id))
    except HTTPNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'System with id {system_id} not found!')


@router_system.delete("/delete/{system_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_system(system_id: int,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    deleted_count = await System.filter(id=system_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"System {system_id} not found")
    return StatusResponse(message=f"Success delete {system_id}")
