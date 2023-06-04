from fastapi.security import HTTPAuthorizationCredentials
from tortoise.functions import Count

from database.models.order import Order
from database.models.user import User
from database.models.status import Status
from fastapi import APIRouter, Depends

from routers.v1.router_auth import auth_schema
from utils.permission import PermissionChecker

router_statistics = APIRouter(prefix="/statistics", tags=["Statistics"])


async def full_statistics_schema(statistic_order):
    creator = await User.get(id=statistic_order["creator_id"])
    status = await Status.get(id=statistic_order["status_id"])
    return {"creator": {"id": creator.id,
                        "name": creator.name,
                        "surname": creator.surname,
                        "role": creator.role,
                        "telephone": creator.telephone},
            "status": {"id": status.id,
                       "status_name": status.status_name},
            "count": statistic_order["count"]}


@router_statistics.get("/")
async def count_orders_of_users(token: HTTPAuthorizationCredentials = Depends(auth_schema),
                                permission: bool = Depends(PermissionChecker(required_permissions=['admin']))):
    statistic_orders = await Order.annotate(group_name=Order.creator, count=Count('id')). \
        prefetch_related('creator', 'status').group_by('creator_id', 'status_id').order_by('-count'). \
        values('creator_id', 'status_id', 'count')
    stat_order_list = []
    for stat_order in statistic_orders:
        stat_order_list.append(await full_statistics_schema(stat_order))
    return stat_order_list
