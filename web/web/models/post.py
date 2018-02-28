# coding:utf-8
from django.db import models
from django.contrib import admin

class Post(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    preview = models.CharField(max_length=512, blank=True, null=True)
    video = models.CharField(max_length=512, blank=True, null=True)
    video_format = models.CharField(max_length=512, blank=True, null=True)
    duration = models.IntegerField()
    category = models.CharField(max_length=512)
    created_at = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    play_counts = models.IntegerField()
    like_counts = models.IntegerField()
    thumbnail = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'posts'

    def __unicode__(self):
        return self.title
 
class PostAdmin(admin.ModelAdmin):
    list_display = ('pid', 'title', 'video_format', 'category', 'created_at', 'play_counts', 'like_counts')
    empty_value_display = '-'

admin.site.register(Post, PostAdmin)