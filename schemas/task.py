from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.task import Task

TaskSchema = pydantic_model_creator(Task, name='BuildingSchema')
TaskSchemaCreate = pydantic_model_creator(Task, name='BuildingCreateSchema', exclude_readonly=True)
TaskSchemaUpdate = pydantic_model_creator(Task, name='BuildingUpdateSchema', exclude_readonly=True)
