from tortoise.models import Model
from tortoise import fields


class Order(Model):
    id = fields.IntField(pk=True)
    order_name = fields.CharField(max_length=200, unique=True, null=False)
    building = fields.ForeignKeyField("models.Building", related_name='orders')
    system = fields.ForeignKeyField("models.System", related_name='orders')
    important = fields.ForeignKeyField("models.Important", related_name='orders')
    materials = fields.JSONField(default=[])
    creator = fields.ForeignKeyField("models.User", related_name='orders')
    status = fields.ForeignKeyField("models.Status", related_name='orders')
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    expected_time = fields.DatetimeField(null=True)
    description = fields.TextField(null=True)

    def __str__(self):
        return f'Order name: {self.order_name} \n' \
               f'Building: {self.building} \n' \
               f'System: {self.system} \n' \
               f'Important: {self.important} \n' \
               f'Materials: {self.materials} \n' \
               f'Creator: {self.creator} \n' \
               f'Status: {self.status} \n' \
               f'Created_at: {self.created_at} \n' \
               f'Modified_at: {self.modified_at} \n' \
               f'Description: {self.description}'
