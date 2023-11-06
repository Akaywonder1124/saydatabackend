# models.py
from tortoise import fields
from tortoise.models import Model


class MediaFile(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    date_created = fields.DatetimeField()
    duration = fields.CharField(max_length=50)
    file_type = fields.CharField(max_length=50)
    text = fields.CharField(max_length=10000000, null=True)

    class Meta:
        table = "media_files"
