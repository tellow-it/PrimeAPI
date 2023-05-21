from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.role import Role

RoleSchema = pydantic_model_creator(Role, name='RoleSchema')
RoleSchemaCreate = pydantic_model_creator(Role, name='RoleCreateSchema', exclude_readonly=True)
RoleSchemaUpdate = pydantic_model_creator(Role, name='RoleUpdateSchema', exclude_readonly=True)
