from typing import List

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from schemas.important import ImportantSchema, ImportantSchemaCreate, ImportantSchemaUpdate
from database.models.important import Important

router_important = APIRouter(prefix="/important", tags=["Important"])


@router_important.get("/", response_model=List[ImportantSchema])
async def get_important_s(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await ImportantSchema.from_queryset(Important.all())


@router_important.post("/create", response_model=ImportantSchema, status_code=201)
async def create_important(important: ImportantSchemaCreate,
                           token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    important_obj = await Important.create(**important.dict(exclude_unset=True))
    return await ImportantSchema.from_tortoise_orm(important_obj)


@router_important.get("/{important_id}", response_model=ImportantSchema,
                      responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_important(building_id: int,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await ImportantSchema.from_queryset_single(Important.get(id=building_id))


@router_important.put(
    "/update/{important_id}", response_model=ImportantSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_important(building_id: int,
                           building: ImportantSchemaUpdate,
                           token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    await Important.filter(id=building_id).update(**building.dict(exclude_unset=True))
    return await ImportantSchema.from_queryset_single(Important.get(id=building_id))


@router_important.delete("/delete/{important_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_building(important_id: int,
                          token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    deleted_count = await Important.filter(id=important_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Important {important_id} not found")
    return Status(message=f"Success delete {important_id}")
