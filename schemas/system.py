from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.system import System

SystemSchema = pydantic_model_creator(System, name='SystemSchema')
SystemSchemaCreate = pydantic_model_creator(System, name='SystemCreateSchema', exclude_readonly=True)
SystemSchemaUpdate = pydantic_model_creator(System, name='SystemUpdateSchema', exclude_readonly=True)
