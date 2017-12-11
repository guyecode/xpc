# coding:utf-8
from django.db import models
from django.contrib import admin


class Code(models.Model):
    code_id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    code = models.BigIntegerField()
    created_at = models.DateTimeField()
    ip = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'codes'

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code_id', 'phone', 'code', 'created_at', 'ip')
    empty_value_display = '-'

admin.site.register(Code, CodeAdmin)
