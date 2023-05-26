from tortoise.models import Model
from tortoise import fields

from database.models.order import Order


class System(Model):
    id = fields.IntField(pk=True)
    system_name = fields.CharField(max_length=200, unique=True, null=False)
    orders: fields.ReverseRelation["Order"]

    def __str__(self):
        return self.system_name
