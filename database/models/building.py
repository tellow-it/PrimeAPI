from tortoise.models import Model
from tortoise import fields


class Building(Model):
    id = fields.IntField(pk=True)
    building_name = fields.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.building_name


