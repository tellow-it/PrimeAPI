from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    role_id: int
    password: str
    telephone: str


class UserSchemaCreate(BaseModel):
    name: str
    surname: str
    role_id: int
    password: str
    telephone: str


class UserSchemaUpdate(BaseModel):
    name: str
    surname: str
    role_id: int
    password: str
    telephone: str
