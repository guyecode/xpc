from django.db import models
from web.models import Model


class Code(models.Model, Model):
    code_id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    code = models.BigIntegerField()
    created_at = models.DateTimeField()
    ip = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'codes'
