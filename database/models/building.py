from tortoise.models import Model
from tortoise import fields
from database.models.order import Order


# from database.models.building import Building
class Building(Model):
    id = fields.IntField(pk=True)
    building_name = fields.CharField(max_length=200, unique=True, null=False)
    orders: fields.ReverseRelation["Order"]

    def __str__(self):
        return self.building_name
