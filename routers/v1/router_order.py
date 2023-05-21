from typing import List
from schemas.response import Status
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from schemas.order import OrderSchema, OrderSchemaCreate, OrderSchemaUpdate
from database.models.order import Order

router_order = APIRouter(prefix="/order", tags=["Orders"])


@router_order.get("/", response_model=List[OrderSchema])
async def get_orders():
    return await OrderSchema.from_queryset(Order.all())


@router_order.post("/create", response_model=OrderSchema, status_code=201)
async def create_order(order: OrderSchemaCreate):
    order_obj = await Order.create(**order.dict(exclude_unset=True))
    return await OrderSchema.from_tortoise_orm(order_obj)


@router_order.get("/{order_id}", response_model=OrderSchema,
                  responses={404: {"model": HTTPNotFoundError}}, status_code=200)
async def get_order(order_id: int):
    return await OrderSchema.from_queryset_single(Order.get(id=order_id))


@router_order.put(
    "/update/{order_id}", response_model=OrderSchema, responses={404: {"model": HTTPNotFoundError}}
)
async def update_order(order_id: int, order: OrderSchemaUpdate):
    await Order.filter(id=order_id).update(**order.dict(exclude_unset=True))
    return await OrderSchema.from_queryset_single(Order.get(id=order_id))


@router_order.delete("/delete/{order_id}", responses={404: {"model": HTTPNotFoundError}})
async def delete_order(order_id: int):
    deleted_count = await Order.filter(id=order_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return Status(message=f"Success delete {order_id}")
