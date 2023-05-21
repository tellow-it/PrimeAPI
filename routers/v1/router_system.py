from typing import List
from schemas.response import Status
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from schemas.system import SystemSchema, SystemSchemaCreate, SystemSchemaUpdate
from database.models.system import System

router_system = APIRouter(prefix="/system", tags=["Systems"])


@router_system.get("/", response_model=List[SystemSchema])
async def get_systems():
    return await SystemSchema.from_queryset(System.all())


@router_system.post("/create", response_model=SystemSchema, status_code=201)
async def create_system(system: SystemSchemaCreate):
    system_obj = await System.create(**system.dict(exclude_unset=True))
    return await SystemSchema.from_tortoise_orm(system_obj)


@router_system.get("/{system_id}", response_model=SystemSchema,
                     responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_system(system_id: int):
    return await SystemSchema.from_queryset_single(System.get(id=system_id))


@router_system.put(
    "/update/{system_id}", response_model=SystemSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_system(system_id: int, system: SystemSchemaUpdate):
    await System.filter(id=system_id).update(**system.dict(exclude_unset=True))
    return await SystemSchema.from_queryset_single(System.get(id=system_id))


@router_system.delete("/delete/{system_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_system(system_id: int):
    deleted_count = await System.filter(id=system_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"System {system_id} not found")
    return Status(message=f"Success delete {system_id}")
