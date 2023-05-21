from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.user import User

UserSchema = pydantic_model_creator(User, name='UserSchema')
UserSchemaCreate = pydantic_model_creator(User, name='UserCreateSchema', exclude_readonly=True)
UserSchemaUpdate = pydantic_model_creator(User, name='UserUpdateSchema', exclude_readonly=True)
