from typing import List
from schemas.response import Status
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.status import StatusSchema, StatusSchemaUpdate, StatusSchemaCreate
from database.models.status import Status

router_auth = APIRouter(prefix="/auth", tags=["Authorization"])