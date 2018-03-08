import pickle
from hashlib import md5
from django.conf import settings
from web.models.composer import Composer
from web.models.copyright import Copyright
from web.models.post import Post
from web.helpers import r


def get_posts_by_cid(cid, num=0):
    cache_key = 'cr_cid_%s' % cid
    posts = [pickle.loads(i) for i in r.lrange(cache_key, 0, -1)]
    if not posts:
        cr_list = Copyright.objects.filter(cid=cid)
        for cr in cr_list:
            post = Post.get(pid=cr.pid)
            post.roles = cr.roles
            posts.append(post)
            r.lpush(cache_key, pickle.dumps(post))
    return posts[:num or -1]


def get_role_in_post(pid, cid):
    cr = Copyright.objects.filter(pid=pid, cid=cid).first()
    return cr.roles


def md5_pwd(phone, password):
    s = '%s%s%s' % (phone, password, settings.SECRET_KEY)
    return md5(s.encode('utf-8')).hexdigest()