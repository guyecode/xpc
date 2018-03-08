from django.db import models
from web.models import Model


class Comment(models.Model, Model):
    commentid = models.IntegerField(primary_key=True)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    avatar = models.CharField(max_length=512, blank=True, null=True)
    uname = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    reply = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comments'