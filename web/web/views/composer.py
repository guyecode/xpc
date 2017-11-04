# coding:utf-8
from web.models.composer import Composer

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    return render(request, 'composer.html', {'composer': composer})