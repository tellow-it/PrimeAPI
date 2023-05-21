from tortoise.contrib.pydantic import pydantic_model_creator
from database.models.building import Building

BuildingSchema = pydantic_model_creator(Building, name='BuildingSchema')
BuildingSchemaCreate = pydantic_model_creator(Building, name='BuildingCreateSchema', exclude_readonly=True)
BuildingSchemaUpdate = pydantic_model_creator(Building, name='BuildingUpdateSchema', exclude_readonly=True)
