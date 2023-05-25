from pydantic import BaseModel


class LoginSchema(BaseModel):
    telephone: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
