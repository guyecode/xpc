# coding:utf-8
from django.db import models
from django.contrib import admin

class Composer(models.Model):
    cid = models.BigIntegerField(primary_key=True)
    banner = models.CharField(max_length=512)
    avatar = models.CharField(max_length=512)
    verified = models.IntegerField()
    name = models.CharField(max_length=128)
    intro = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    fans_counts = models.IntegerField()
    follow_counts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'composers'

    def __unicode__(self):
        return self.title


class ComposerAdmin(admin.ModelAdmin):
    list_display = ('cid', 'name', 'verified', 'intro', 'fans_counts', 'like_counts', 'follow_counts')
    empty_value_display = '-'

admin.site.register(Composer, ComposerAdmin)