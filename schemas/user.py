from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class UserSchema(BaseModel):
    name: str
    surname: str
    role: str
    password: Optional[str]
    telephone: str


class UserSchemaRead(UserSchema):
    id: int


class UserUpdatePassword(BaseModel):
    password: str
    new_password: str
