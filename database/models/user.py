from enum import Enum

from tortoise.models import Model
from tortoise import fields

from database.models.role import Roles


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    surname = fields.CharField(max_length=100, null=False)
    role = fields.CharEnumField(Roles)
    password = fields.CharField(max_length=200, null=False)
    telephone = fields.CharField(max_length=11, null=False, unique=True)

    def __str__(self):
        return f'Surname: {self.surname} \n' \
               f'Name: {self.name} \n' \
               f'Telephone: {self.telephone} \n' \
               f'Role_id: {self.role}'
