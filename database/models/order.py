from tortoise.models import Model
from tortoise import fields

class Order(Model):
    id = fields.IntField(pk=True)
    building = fields.ForeignKeyField("models.Building", related_name='tasks', on_delete='CASCADE')
    system = fields.ForeignKeyField("models.System", related_name='tasks')
    important = fields.ForeignKeyField("models.Important", related_name='tasks')
    material = fields.TextField(null=False)
    quantity = fields.IntField(null=False)
    creator = fields.ForeignKeyField("models.User", related_name='tasks')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    expected_time = fields.CharField(null=True, max_length=100)

    def __str__(self):
        return f'Building: {self.building} \n' \
               f'System: {self.system} \n' \
               f'Important: {self.important} \n' \
               f'Material: {self.material} \n' \
               f'Quantity: {self.quantity} \n' \
               f'Creator: {self.creator} \n' \
               f'Created_at: {self.created_at} \n' \
               f'Modified_at: {self.modified_at} \n' \
               f'End_at: {self.end_at}'
