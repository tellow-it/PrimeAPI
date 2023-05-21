from typing import List
from schemas.response import Status
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

router_task = APIRouter(prefix="/task", tags=["Tasks"])
