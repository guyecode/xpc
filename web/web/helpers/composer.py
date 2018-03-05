from web.models.composer import Composer
from web.models.copyright import Copyright
from web.models.post import Post


def get_posts_by_cid(cid, num=0):
    if num:
        cr_list = Copyright.objects.filter(cid=cid)[:num]
    else:
        cr_list = Copyright.objects.filter(cid=cid).all()
    posts = []
    for cr in cr_list:
        post = Post.get(pid=cr.pid)
        post.roles = cr.roles
        posts.append(post)
    return posts


def get_role_in_post(pid, cid):
    cr = Copyright.objects.filter(pid=pid, cid=cid).first()
    return cr.roles


