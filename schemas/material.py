from pydantic import BaseModel


class MaterialSchema(BaseModel):
    material: str
    quantity: int
