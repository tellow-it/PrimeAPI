from typing import List, Optional

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import StatusResponse
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.status import StatusSchema, StatusSchemaUpdate, StatusSchemaCreate
from database.models.status import Status
from utils.permission import PermissionChecker

router_status = APIRouter(prefix="/status", tags=["Statuses"])


@router_status.get("/", response_model=List[StatusSchema],
                   description="""
                   В поле order_by_field нужно передать поле по которому нужно сделать сортировку
                   в следующем формате:
                   \n1) порядок сортировки, если по убыванию, то перед названием поля нужно поставить "-", иначе ничего не ставить
                   \n2) поле по которому будет сортировка, вот список полей, которые которые можно передать чтобы отсортировать данные в зависимости от колонки:\n
                   Название статуса(по нему сортируется по умолчанию "status_name"): status_name\n
                   """)
async def get_statuses(order_by_field: Optional[str] = "status_name",
                       token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await StatusSchema.from_queryset(Status.all().order_by(order_by_field))


@router_status.post("/create", response_model=StatusSchema, status_code=201)
async def create_status(status: StatusSchemaCreate,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    status_obj = await Status.create(**status.dict(exclude_unset=True))
    return await StatusSchema.from_tortoise_orm(status_obj)


@router_status.get("/{status_id}", response_model=StatusSchema,
                   responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_status(status_id: int,
                     token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await StatusSchema.from_queryset_single(Status.get(id=status_id))


@router_status.put(
    "/update/{status_id}", response_model=StatusSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_status(status_id: int, status: StatusSchemaUpdate,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    await Status.filter(id=status_id).update(**status.dict(exclude_unset=True))
    return await StatusSchema.from_queryset_single(Status.get(id=status_id))


@router_status.delete("/delete/{status_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_status(status_id: int,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema),
                        permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    deleted_count = await Status.filter(id=status_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Status {status_id} not found")
    return StatusResponse(message=f"Success delete {status_id}")
