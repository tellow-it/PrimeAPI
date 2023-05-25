# from tortoise.models import Model
# from tortoise import fields
from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    user = "user"
    advanced_user = "advanced_user"

# class Role(Model):
#     id = fields.IntField(pk=True)
#     role_name = fields.CharEnumField(Roles)
#
#     def __str__(self):
#         return self.role_name
