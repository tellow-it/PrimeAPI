from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.important import Important

ImportantSchema = pydantic_model_creator(Important, name='ImportantSchema')
ImportantSchemaCreate = pydantic_model_creator(Important, name='ImportantCreateSchema', exclude_readonly=True)
ImportantSchemaUpdate = pydantic_model_creator(Important, name='ImportantUpdateSchema', exclude_readonly=True)
