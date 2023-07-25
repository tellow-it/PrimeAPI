from typing import List, Optional

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import StatusResponse
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from schemas.important import ImportantSchema, ImportantSchemaCreate, ImportantSchemaUpdate
from database.models.important import Important
from utils.permission import PermissionChecker

router_important = APIRouter(prefix="/important", tags=["Important"])


@router_important.get("/", response_model=List[ImportantSchema],
                      description="""
                   В поле order_by_field нужно передать поле по которому нужно сделать сортировку
                   в следующем формате:
                   \n1) порядок сортировки, если по убыванию, то перед названием поля нужно поставить "-", иначе ничего не ставить
                   \n2) поле по которому будет сортировка, вот список полей, которые которые можно передать чтобы отсортировать данные в зависимости от колонки:\n
                   Название срочности(по нему сортируется по умолчанию "important_name"): important_name\n
                   """)
async def get_important_s(order_by_field: Optional[str] = "important_name",
                          token: HTTPAuthorizationCredentials = Depends(auth_schema), ):
    return await ImportantSchema.from_queryset(Important.all().order_by(order_by_field))


@router_important.post("/create", response_model=ImportantSchema, status_code=201)
async def create_important(important: ImportantSchemaCreate,
                           token: HTTPAuthorizationCredentials = Depends(auth_schema),
                           permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    important_obj = await Important.create(**important.dict(exclude_unset=True))
    return await ImportantSchema.from_tortoise_orm(important_obj)


@router_important.get("/{important_id}", response_model=ImportantSchema,
                      responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_important(important_id: int,
                        token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await ImportantSchema.from_queryset_single(Important.get(id=important_id))


@router_important.put(
    "/update/{important_id}", response_model=ImportantSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_important(important_id: int,
                           important: ImportantSchemaUpdate,
                           token: HTTPAuthorizationCredentials = Depends(auth_schema),
                           permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    await Important.filter(id=important_id).update(**important.dict(exclude_unset=True))
    return await ImportantSchema.from_queryset_single(Important.get(id=important_id))


@router_important.delete("/delete/{important_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_building(important_id: int,
                          token: HTTPAuthorizationCredentials = Depends(auth_schema),
                          permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    deleted_count = await Important.filter(id=important_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Important {important_id} not found")
    return StatusResponse(message=f"Success delete {important_id}")
