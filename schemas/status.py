from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.status import Status

StatusSchema = pydantic_model_creator(Status, name='StatusSchema')
StatusSchemaCreate = pydantic_model_creator(Status, name='StatusCreateSchema', exclude_readonly=True)
StatusSchemaUpdate = pydantic_model_creator(Status, name='StatusUpdateSchema', exclude_readonly=True)
