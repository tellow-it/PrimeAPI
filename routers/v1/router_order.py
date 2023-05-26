from typing import List

from fastapi.security import HTTPAuthorizationCredentials
from tortoise.contrib.pydantic import pydantic_model_creator

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.order import OrderSchema, OrderSchemaRead, normal_prefetch
from database.models.order import Order
import json

router_order = APIRouter(prefix="/order", tags=["Orders"])


@router_order.get("/", response_model=List)
async def get_orders(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    orders = await Order.all().prefetch_related("building", "important", "creator", "system")
    order_list = []
    for order in orders:
        order_info = normal_prefetch(order)
        order_list.append(order_info)
    return order_list


@router_order.post("/create", response_model=OrderSchemaRead, status_code=201)
async def create_order(order: OrderSchema,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    order_obj = await Order.create(**order.dict(exclude_unset=True))
    return order_obj


@router_order.get("/{order_id}", responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_order(order_id: int,
                    token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    order = await Order.get(id=order_id).prefetch_related("building", "important", "creator", "system")
    return normal_prefetch(order)


@router_order.put(
    "/update/{order_id}", response_model=OrderSchemaRead, responses={404: {"model": HTTPNotFoundError}}
)
async def update_order(order_id: int,
                       order: OrderSchema,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    await Order.filter(id=order_id).update(**order.dict(exclude_unset=True))
    return await Order.get(id=order_id)


@router_order.delete("/delete/{order_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_order(order_id: int,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    deleted_count = await Order.filter(id=order_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return Status(message=f"Success delete {order_id}")
