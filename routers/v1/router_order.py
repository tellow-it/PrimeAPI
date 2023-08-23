from datetime import datetime, timezone
from typing import List, Optional
from fastapi.security import HTTPAuthorizationCredentials

from database.models.status import Status
from routers.v1.router_auth import auth_schema
from schemas.response import StatusResponse
from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.order import OrderSchema, OrderSchemaRead, normal_prefetch
from database.models.order import Order
from utils.jwt import decode_access_token
from utils.permission import PermissionChecker

router_order = APIRouter(prefix="/order", tags=["Orders"])


@router_order.get("/", status_code=200,
                  description="""
                   В поле order_by_field нужно передать поле по которому нужно сделать сортировку
                   в следующем формате:
                   \n1) порядок сортировки, если по убыванию, то перед названием поля нужно поставить "-", иначе ничего не ставить
                   \n2) поле по которому будет сортировка, вот список полей, которые которые можно передать чтобы отсортировать данные в зависимости от колонки:\n
                   Дата создание(по нему сортируется по умолчанию "created_at"): created_at\n
                   Создатель: creator__surname\n
                   Объект: building__building_name\n
                   Материалы и их количество: materials\n
                   """)
async def get_orders(on_page: Optional[int] = 10,
                     page: Optional[int] = 0,
                     search_by_material: Optional[str] = None,
                     order_by_field: Optional[str] = "-created_at",
                     token: HTTPAuthorizationCredentials = Depends(auth_schema),
                     ):
    user_info = decode_access_token(token)
    if user_info['role'] == 'admin':
        if search_by_material is not None:
            quantity_orders = await Order.filter(material__icontains=f'{search_by_material}').all().count()
            orders = await Order.filter(material__icontains=f'{search_by_material}').all(). \
                order_by(order_by_field).offset(page * on_page).limit(on_page). \
                prefetch_related("building", "important", "creator", "system", "status")
        else:
            quantity_orders = await Order.all().count()
            orders = await Order.all().order_by(order_by_field).offset(page * on_page). \
                limit(on_page).prefetch_related("building", "important", "creator", "system", "status")
    else:
        if search_by_material is not None:
            quantity_orders = await Order.filter(creator_id=user_info['id']).filter(
                material__contains=f'{search_by_material}').all().count()
            orders = await Order.filter(creator_id=user_info['id']).filter(
                material__contains=f'{search_by_material}').all().order_by(order_by_field).offset(page * on_page). \
                limit(on_page).prefetch_related("building", "important", "creator", "system", "status")
        else:
            quantity_orders = await Order.filter(creator_id=user_info['id']).count()
            orders = await Order.filter(creator_id=user_info['id']).order_by(order_by_field). \
                offset(page * on_page).limit(on_page). \
                prefetch_related("building", "important", "creator", "system", "status")
    order_list = []
    for order in orders:
        order_info = normal_prefetch(order)
        order_list.append(order_info)
    return {"quantity_orders": quantity_orders,
            "orders": order_list}


@router_order.get("/for-user/{user_id}", status_code=200)
async def get_orders_by_user_id(user_id: int,
                                on_page: Optional[int] = 10,
                                page: Optional[int] = 0,
                                order_by_field: Optional[str] = "created_at",
                                token: HTTPAuthorizationCredentials = Depends(auth_schema),
                                permission: bool = Depends(
                                    PermissionChecker(required_permissions=['admin']))
                                ):
    quantity_orders = await Order.all().filter(creator_id=user_id).count()
    orders = await Order.all().filter(creator_id=user_id).order_by(order_by_field).offset(page * on_page). \
        limit(on_page).prefetch_related("building", "important", "creator", "system", "status")
    order_list = []
    for order in orders:
        order_info = normal_prefetch(order)
        order_list.append(order_info)
    return {"quantity_orders": quantity_orders,
            "order_list": order_list}


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
    order_dict = order.dict(exclude_unset=True)
    order_dict["modified_at"] = datetime.now(timezone.utc)
    if user_info['role'] == 'advanced_user':
        order_obj = await Order.get(id=order_id).prefetch_related('creator')
        if user_info['id'] == order_obj.creator.id:
            await Order.filter(id=order_id).update(**order_dict)
            return await Order.get(id=order_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')
    else:
        await Order.filter(id=order_id).update(**order_dict)
        return await Order.get(id=order_id)


@router_order.patch(
    "/update-status/{order_id}", response_model=OrderSchemaRead, responses={404: {"model": HTTPNotFoundError}}
)
async def update_status_order(order_id: int,
                              status_id: int,
                              token: HTTPAuthorizationCredentials = Depends(auth_schema),
                              permission: bool = Depends(
                                  PermissionChecker(required_permissions=['admin', 'advanced_user']))):
    user_info = decode_access_token(token)
    status_obj = await Status.get(id=status_id)
    order_obj = await Order.get(id=order_id)
    if user_info['role'] == 'advanced_user':
        if user_info['id'] == order_obj.creator.id:
            await order_obj.update_from_dict({'status_id': status_id,
                                              'modified_at': datetime.now(timezone.utc)}).save()
            return await Order.get(id=order_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='The user does not have access to the resource')
    else:
        await order_obj.update_from_dict({'status_id': status_id,
                                          'modified_at': datetime.now(timezone.utc)}).save()
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
    return StatusResponse(message=f"Success delete {order_id}")
