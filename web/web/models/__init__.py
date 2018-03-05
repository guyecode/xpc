import pickle
from web.helpers import r


class Model(object):
    @classmethod
    def get(cls, **kwargs):
        cache_key = '%s_%s' % (cls.__name__, next(iter(kwargs.values())))
        post = r.get(cache_key)
        if post:
            return pickle.loads(post)
        obj = cls.objects.get(**kwargs)
        r.set(cache_key, pickle.dumps(obj))
        return obj