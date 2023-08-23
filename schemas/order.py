from datetime import timezone
from typing import Optional, List
from pydantic.schema import datetime
from pydantic import BaseModel, Json
from schemas.material import MaterialSchema


class OrderSchema(BaseModel):
    building_id: int
    system_id: int
    important_id: int
    materials: Json = []
    creator_id: int
    status_id: int
    expected_time: Optional[datetime] = None
    description: Optional[str] = None


class OrderSchemaRead(OrderSchema):
    id: int
    created_at: datetime
    modified_at: datetime


def normal_prefetch(order):
    prefetch_order = {
        'id': order.id,
        'building': {'id': order.building.id,
                     'building_name': order.building.building_name},
        'system': {'id': order.system.id,
                   'system_name': order.system.system_name},
        'important': {'id': order.important.id,
                      'important_name': order.important.important_name},
        'materials': order.materials,
        'creator': {'id': order.creator.id,
                    "name": order.creator.name,
                    "surname": order.creator.surname,
                    "role": order.creator.role,
                    "telephone": order.creator.telephone
                    },
        'status': {'id': order.status.id,
                   'status_name': order.status.status_name},
        'created_at': order.created_at,
        'modified_at': order.modified_at,
        'expected_time': order.expected_time,
        'description': order.description
    }
    return prefetch_order
