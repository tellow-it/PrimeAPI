from typing import Optional
from pydantic.schema import datetime
from pydantic import BaseModel


class OrderSchema(BaseModel):
    building_id: int
    system_id: int
    important_id: int
    material: str
    quantity: int
    creator_id: int
    created_at: datetime
    modified_at: datetime
    expected_time: Optional[datetime]


class OrderSchemaRead(OrderSchema):
    id: int
