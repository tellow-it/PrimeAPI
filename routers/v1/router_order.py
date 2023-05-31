from typing import List, Optional
from fastapi.security import HTTPAuthorizationCredentials
from tortoise.expressions import Q

from routers.v1.router_auth import auth_schema
from schemas.response import Status
from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.order import OrderSchema, OrderSchemaRead, normal_prefetch
from database.models.order import Order
from utils.jwt import decode_access_token
from utils.permission import PermissionChecker

router_order = APIRouter(prefix="/order", tags=["Orders"])


@router_order.get("/", response_model=List, status_code=200)
async def get_orders(on_page: Optional[int] = 10,
                     page: Optional[int] = 0,
                     search_by_material: Optional[str] = None,
                     token: HTTPAuthorizationCredentials = Depends(auth_schema),

                     ):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        if search_by_material is not None:
            orders = await Order.filter(material__contains=f'{search_by_material}').all().offset(page * on_page).limit(
                on_page).prefetch_related("building", "important", "creator", "system", "status")
        else:
            orders = await Order.all().offset(page * on_page).limit(
                on_page).prefetch_related("building", "important", "creator", "system", "status")
        order_list = []
        for order in orders:
            order_info = normal_prefetch(order)
            order_list.append(order_info)
        return order_list
    else:
        orders = await Order.filter(creator_id=user_info['id']). \
            offset(page * on_page).limit(on_page).prefetch_related("building", "important", "creator", "system",
                                                                   "status")
        order_list = []
        for order in orders:
            order_info = normal_prefetch(order)
            order_list.append(order_info)
        return order_list


@router_order.get("/for-user/{user_id}", response_model=List, status_code=200)
async def get_orders_by_user_id(user_id: int,
                                on_page: Optional[int] = 10,
                                page: Optional[int] = 0,
                                token: HTTPAuthorizationCredentials = Depends(auth_schema),
                                permission: bool = Depends(
                                    PermissionChecker(required_permissions=['admin']))
                                ):
    orders = await Order.all().filter(creator_id=user_id).offset(page * on_page).limit(
        on_page).prefetch_related("building", "important",
                                  "creator", "system", "status")
    order_list = []
    for order in orders:
        order_info = normal_prefetch(order)
        order_list.append(order_info)
    return order_list


@router_order.post("/create", response_model=OrderSchemaRead, status_code=201)
async def create_order(order: OrderSchema,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema),
                       ):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        order_obj = await Order.create(**order.dict(exclude_unset=True))
        return order_obj
    else:
        if user_info['id'] == order.creator_id:
            order_obj = await Order.create(**order.dict(exclude_unset=True))
            return order_obj
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')


@router_order.get("/{order_id}", responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_order(order_id: int,
                    token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        order = await Order.get(id=order_id).prefetch_related("building", "important", "creator", "system", "status")
        return normal_prefetch(order)
    else:
        order = await Order.get(id=order_id).prefetch_related("building", "important", "creator", "system", "status")
        if user_info['id'] == order.creator.id:
            return normal_prefetch(order)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')


@router_order.put(
    "/update/{order_id}", response_model=OrderSchemaRead, responses={404: {"model": HTTPNotFoundError}}
)
async def update_order(order_id: int,
                       order: OrderSchema,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema),
                       permission: bool = Depends(PermissionChecker(required_permissions=['admin', 'advanced_user']))):
    user_info = decode_access_token(token)
    if user_info['role'] == 'advanced_user':
        order_obj = await Order.get(id=order_id).prefetch_related('creator')
        if user_info['id'] == order_obj.creator.id:
            await Order.filter(id=order_id).update(**order.dict(exclude_unset=True))
            return await Order.get(id=order_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')
    else:
        await Order.filter(id=order_id).update(**order.dict(exclude_unset=True))
        return await Order.get(id=order_id)


@router_order.delete("/delete/{order_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_order(order_id: int,
                       token: HTTPAuthorizationCredentials = Depends(auth_schema),
                       permission: bool = Depends(PermissionChecker(required_permissions=['admin', 'advanced_user']))):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        deleted_count = await Order.filter(id=order_id).delete()
    else:
        order_obj = await Order.get(id=order_id).prefetch_related('creator')
        if user_info['id'] == order_obj.creator.id:
            deleted_count = await Order.filter(id=order_id).delete()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return Status(message=f"Success delete {order_id}")
