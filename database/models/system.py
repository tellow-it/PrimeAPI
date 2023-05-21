from tortoise.models import Model
from tortoise import fields


class System(Model):
    id = fields.IntField(pk=True)
    system_name = fields.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.system_name
