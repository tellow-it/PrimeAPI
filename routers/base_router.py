from routers.v1.router_buildings import router_building
from routers.v1.router_important import router_important
from routers.v1.router_roles import router_role
from routers.v1.router_system import router_system
from routers.v1.router_status import router_status
from routers.v1.router_statistics import router_statistics
from routers.v1.router_tasks import router_task
from routers.v1.router_auth import router_auth
from fastapi import APIRouter

main_router = APIRouter(prefix="/v1")

main_router.include_router(router_auth)
main_router.include_router(router_task)
main_router.include_router(router_building)
main_router.include_router(router_important)
main_router.include_router(router_status)
main_router.include_router(router_system)
main_router.include_router(router_role)
main_router.include_router(router_statistics)
