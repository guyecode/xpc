from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.functional import cached_property
from web.models.post import Post
from web.models.comment import Comment
from web.helpers.composer import get_posts_by_cid
from web.helpers import r
from django.views.decorators.cache import cache_page

@cached_property
def count(self):
    posts_count = r.get('posts_count')
    if not posts_count:
        posts_count = self.object_list.count()
        r.set('posts_count', posts_count)

    return int(posts_count)

Paginator.count = count


@cache_page(60)
def show_list(request):
    post_list = Post.objects.order_by('-play_counts')
    paginator = Paginator(post_list, 40)
    posts = paginator.page(1)
    for post in posts:
        post.composers = post.get_composers()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pid):
    post = Post.get(pid=pid)
    post.composers = post.get_composers()
    composer = post.first_composer
    composer.posts = get_posts_by_cid(composer.cid, 6)
    return render(request, 'post.html', locals())


def get_comments(request):
    pid = request.GET.get('id')
    page = request.GET.get('page')
    comment_list = Comment.objects.filter(pid=pid).order_by('-created_at')
    paginator = Paginator(comment_list, 10)
    comments = paginator.page(page)
    return render(request, 'comments.html', locals())
