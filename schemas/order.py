from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.order import Order

OrderSchema = pydantic_model_creator(Order, name='OrderSchema')
OrderSchemaCreate = pydantic_model_creator(Order, name='OrderCreateSchema', exclude_readonly=True)
OrderSchemaUpdate = pydantic_model_creator(Order, name='OrderUpdateSchema', exclude_readonly=True)
