from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    surname = fields.CharField(max_length=100, null=False)
    role = fields.ForeignKeyField("models.Role", related_name='users')
    password = fields.CharField(max_length=200, null=False)
    telephone = fields.CharField(max_length=11, null=False, unique=True)

    def __str__(self):
        return f'{self.surname} {self.name} - {self.telephone}'
