# coding:utf-8
from web.models.post import Post

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


def show_list(request):
    if request.GET.get('err'):
        1 / 0
    posts = Post.objects.order_by('-play_counts')[:16]
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pid):
    post = Post.objects.get(pid=pid)
    return render(request, 'post.html', {'post': post})