from django.http import HttpResponseRedirect
from django.conf import settings
from web.models.composer import Composer
from web.helpers.composer import md5_pwd
need_login = ['/']


class AuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path in need_login:
            cid = request.COOKIES.get('cid')
            token = request.COOKIES.get('token')
            if not cid or md5_pwd(cid, settings.SECRET_KEY) != token:
                return HttpResponseRedirect('/login/')
            request.composer = Composer.get(cid=cid)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response