"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from web.views import post, composer


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post.show_list),
    url(r'^register/', composer.register),
    url(r'^login/', composer.login),
    url(r'^api/v1/user/register', composer.do_register),
    url(r'^api/v1/user/login', composer.do_login),
    url(r'^api/v1/mobile/send', composer.send_code),
    url(r'^user/login/ts-out', composer.logout),
    url(r'^find_password', composer.find_password),
    url(r'^api/v1/user/check/send', composer.check_send),
    url(r'^api/v1/mobile/check/find', composer.mobile_check),
    url(r'^api/v1/user/findPwd', composer.reset_pwd),

    url(r'^user/oneuser/userid-(?P<cid>\d+)$', composer.oneuser),
    url(r'^a(?P<pid>\d+)$', post.post_detail),
    url(r'^article/filmplay/ts-getCommentApi/$', post.get_comments),
    url(r'^u(?P<cid>\d+)$', composer.homepage)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns