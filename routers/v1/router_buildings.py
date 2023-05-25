from typing import List

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

from schemas.bulding import BuildingSchema, BuildingSchemaCreate, BuildingSchemaUpdate
from database.models.building import Building

router_building = APIRouter(prefix="/building", tags=["Buildings"])


@router_building.get("/", response_model=List[BuildingSchema])
async def get_buildings(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await BuildingSchema.from_queryset(Building.all())


@router_building.post("/create", response_model=BuildingSchema, status_code=201)
async def create_building(building: BuildingSchemaCreate,
                          token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    building_obj = await Building.create(**building.dict(exclude_unset=True))
    return await BuildingSchema.from_tortoise_orm(building_obj)


@router_building.get("/{building_id}", response_model=BuildingSchema,
                     responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_building(building_id: int,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return await BuildingSchema.from_queryset_single(Building.get(id=building_id))


@router_building.put(
    "/update/{building_id}", response_model=BuildingSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_building(building_id: int,
                          building: BuildingSchemaUpdate,
                          token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    await Building.filter(id=building_id).update(**building.dict(exclude_unset=True))
    return await BuildingSchema.from_queryset_single(Building.get(id=building_id))


@router_building.delete("/delete/{building_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_building(building_id: int,
                          token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    deleted_count = await Building.filter(id=building_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Building {building_id} not found")
    return Status(message=f"Success delete {building_id}")
