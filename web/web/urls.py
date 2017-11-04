"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import debug_toolbar
from web.views import post, composer


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', post.show_list, name='index'),
    url(r'^post/list/', post.show_list),
    url(r'^a(?P<pid>\d+)/', post.post_detail),
    url(r'^composer/(?P<cid>\d+)/', composer.homepage),
]


urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]