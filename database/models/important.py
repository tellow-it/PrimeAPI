from tortoise.models import Model
from tortoise import fields

from database.models.order import Order


class Important(Model):
    id = fields.IntField(pk=True)
    important_name = fields.CharField(max_length=200, unique=True, null=False)
    orders: fields.ReverseRelation["Order"]

    def __str__(self):
        return self.important_name
