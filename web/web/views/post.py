# coding:utf-8
from web.models.post import Post
from web.models.comment import Comment
from web.models.copyright import Copyright
import redis
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.functional import cached_property


POSTS_PER_PAGE = 32
r = redis.StrictRedis()


@cached_property
def count(self):
    posts_count = r.get('posts_count')
    if not posts_count:
        posts_count = self.object_list.count()
        r.set('posts_count', posts_count)
    return int(posts_count)

Paginator.count = count

def index(request):
    return redirect('/post/list/hot/')


def show_list(request, sort='hot', page=1):
    sorted_col = None
    if sort == 'hot':
        sorted_col = '-play_counts'
    elif sort == 'newest':
        sorted_col = '-created_at'
    elif sort == 'popular':
        sorted_col = '-like_counts'
    post_list = Post.objects.order_by(sorted_col)
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    posts = paginator.page(int(page))
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pid):
    post = Post.objects.get(pid=pid)
    return render(request, 'post.html', {'post': post})
