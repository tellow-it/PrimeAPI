from tortoise.models import Model
from tortoise import fields


class Status(Model):
    id = fields.IntField(pk=True)
    status_name = fields.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.status_name
