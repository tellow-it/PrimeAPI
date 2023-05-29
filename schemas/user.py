from typing import Optional
from pydantic.schema import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    surname: str
    role: str
    password: Optional[str]
    telephone: str
    created_at: datetime


class UserSchemaRead(UserSchema):
    id: int


class UserUpdatePassword(BaseModel):
    password: str
    new_password: str
