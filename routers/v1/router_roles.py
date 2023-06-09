from fastapi.security import HTTPAuthorizationCredentials
from routers.v1.router_auth import auth_schema
from fastapi import APIRouter, Depends
from database.models.role import Roles

router_role = APIRouter(prefix="/role", tags=["Roles"])


@router_role.get("/")
async def get_roles(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return {"roles": [Roles.admin.name, Roles.user.name, Roles.advanced_user.name]}
