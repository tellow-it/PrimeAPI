from typing import List

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.status import StatusSchema, StatusSchemaUpdate, StatusSchemaCreate
from database.models.status import Status

router_status = APIRouter(prefix="/status", tags=["Statuses"])


@router_status.get("/", response_model=List[StatusSchema])
async def get_statuses(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await StatusSchema.from_queryset(Status.all())


@router_status.post("/create", response_model=StatusSchema, status_code=201)
async def create_status(status: StatusSchemaCreate,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema)):
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
                        token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    await Status.filter(id=status_id).update(**status.dict(exclude_unset=True))
    return await StatusSchema.from_queryset_single(Status.get(id=status_id))


@router_status.delete("/delete/{status_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_status(status_id: int,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    deleted_count = await Status.filter(id=status_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Status {status_id} not found")
    return Status(message=f"Success delete {status_id}")
