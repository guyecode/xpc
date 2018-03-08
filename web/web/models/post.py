import pickle
from django.db import models
from web.models import Model
from web.models.composer import Composer
from web.models.copyright import Copyright
from web.helpers import r


class Post(models.Model, Model):
    pid = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    preview = models.CharField(max_length=512, blank=True, null=True)
    video = models.CharField(max_length=512, blank=True, null=True)
    video_format = models.CharField(max_length=512, blank=True, null=True)
    category = models.CharField(max_length=512)
    created_at = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    play_counts = models.IntegerField()
    like_counts = models.IntegerField()
    thumbnail = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'

    def get_composers(self):
        cache_key = 'cr_pid_%s' % self.pid
        composers = [pickle.loads(i) for i in r.lrange(cache_key, 0, -1)]
        if not composers:
            cr_list = Copyright.objects.filter(pid=self.pid).all()
            for cr in cr_list:
                composer = Composer.get(cid=cr.cid)
                if composer:
                    composer.role = cr.roles
                    composers.append(composer)
                    r.lpush(cache_key, pickle.dumps(composer))
        return composers
