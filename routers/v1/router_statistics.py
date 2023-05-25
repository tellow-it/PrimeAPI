from typing import List

from fastapi.security import HTTPAuthorizationCredentials

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.status import StatusSchema, StatusSchemaUpdate, StatusSchemaCreate
from database.models.status import Status

router_statistics = APIRouter(prefix="/statistics", tags=["Statistics"])
