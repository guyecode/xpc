from django.db import models
from web.models import Model


class Copyright(models.Model, Model):
    pcid = models.CharField(primary_key=True, max_length=32)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    roles = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'copyrights'