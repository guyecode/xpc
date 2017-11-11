# coding:utf-8
from web.models.post import Post

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


POSTS_PER_PAGE = 32

def show_list(request, page=1):
    if request.GET.get('err'):
        1 / 0
    post_list = Post.objects.order_by('-play_counts')
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    posts = paginator.page(page)
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pid):
    post = Post.objects.get(pid=pid)
    return render(request, 'post.html', {'post': post})