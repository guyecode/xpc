from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist


class Model(object):

    @classmethod
    def get(cls, **kwargs):
        cache_key = '%s_%s' % (cls.__name__, next(iter(kwargs.values())))
        obj = cache.get(cache_key)
        if not obj:
            try:
                # obj = cls.objects.filter(**kwargs).first()
                obj = cls.objects.get(**kwargs)
            except ObjectDoesNotExist:
                return None
            if obj:
                cache.set(cache_key, obj)
        return obj