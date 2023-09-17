from typing import Optional
from pydantic.schema import datetime
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str
    surname: str
    role: str
    password: Optional[str] = Field(min_length=5)
    telephone: str
    created_at: datetime


class UserSchemaRead(UserSchema):
    id: int


class UserUpdatePassword(BaseModel):
    password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)
