from django.db import models
from web.models import Model


class Composer(models.Model, Model):
    cid = models.BigIntegerField(primary_key=True)
    banner = models.CharField(max_length=512, null=True)
    avatar = models.CharField(max_length=512, null=True)
    verified = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    intro = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField(default=0)
    fans_counts = models.IntegerField(default=0)
    follow_counts = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'composers'

    @classmethod
    def get_by_phone(cls, phone):
        return cls.objects.filter(phone=phone).first()