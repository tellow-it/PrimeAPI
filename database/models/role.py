from tortoise.models import Model
from tortoise import fields


class Role(Model):
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.role_name
