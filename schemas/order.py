from datetime import timezone
from typing import Optional, List
from pydantic.schema import datetime
from pydantic import BaseModel, Json
from schemas.material import MaterialSchema
from database.models.order import Order


class OrderSchema(BaseModel):
    order_name: str
    building_id: int
    system_id: int
    important_id: int
    materials: List[MaterialSchema] = []
    creator_id: int
    status_id: int
    expected_time: Optional[datetime] = None
    description: Optional[str] = None


class OrderSchemaRead(OrderSchema):
    id: int
    created_at: datetime
    modified_at: datetime


def normal_prefetch(order: Order):
    prefetch_order = {
        'id': order.id,
        'order_name': order.order_name,
        'materials': order.materials,
        'created_at': order.created_at,
        'modified_at': order.modified_at,
        'expected_time': order.expected_time,
        'description': order.description
    }

    if order.building:
        prefetch_order['building'] = {'id': order.building.id,
                                      'building_name': order.building.building_name}
    elif not order.building:
        prefetch_order['building'] = {'id': None,
                                      'building_name': "Удалено"}

    if order.system:
        prefetch_order['system'] = {'id': order.system.id,
                                    'system_name': order.system.system_name}
    elif not order.system:
        prefetch_order['system'] = {'id': None,
                                    'system_name': "Удалено"}

    if order.creator:
        prefetch_order["creator"] = {'id': order.creator.id,
                                     "name": order.creator.name,
                                     "surname": order.creator.surname,
                                     "role": order.creator.role,
                                     "telephone": order.creator.telephone
                                     }
    elif not order.creator:
        prefetch_order["creator"] = {'id': None,
                                     "name": "Удален",
                                     "surname": "Удален",
                                     "role": "Удален",
                                     "telephone": "Удален"
                                     }

    if order.important:
        prefetch_order["important"] = {'id': order.important.id,
                                       'important_name': order.important.important_name}
    elif not order.important:
        prefetch_order["important"] = {'id': None,
                                       'important_name': "Удалено"}

    if order.status:
        prefetch_order["status"] = {'id': order.status.id,
                                    'status_name': order.status.status_name}
    elif not order.status:
        prefetch_order["status"] = {'id': None,
                                    'status_name': "Удалено"}
    return prefetch_order

