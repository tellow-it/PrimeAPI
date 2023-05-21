from tortoise.models import Model
from tortoise import fields


class Important(Model):
    id = fields.IntField(pk=True)
    important = fields.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.important
