import random
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from web.helpers.code import gen_code, verify
from web.helpers.tasks import send_sms_code
from web.models.composer import Composer
from web.models.code import Code
from web.helpers.composer import get_posts_by_cid, md5_pwd


def oneuser(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.posts = get_posts_by_cid(cid, 2)
    return render(request, 'oneuser.html', locals())


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.posts = get_posts_by_cid(cid)
    composer.rest_posts = composer.posts[1:]
    return render(request, 'homepage.html', locals())


def register(request):
    return render(request, 'register.html')


def do_register(request):
    nickname = request.POST.get('nickname')
    phone = request.POST.get('phone')
    code = request.POST.get('code')
    password = request.POST.get('password')
    prefix_code = request.POST.get('prefix_code')
    callback = request.POST.get('callback')
    if Composer.objects.filter(phone=phone).exists():
        data = {"status": -1025, "msg": "该手机号已注册过"}
        return JsonResponse(data)
    if not verify(phone, code):
        return JsonResponse({"status": -1, "msg": "手机验证失败"})

    composer = Composer()
    composer.cid = composer.phone = phone
    composer.name = nickname
    composer.password = md5_pwd(phone, password)
    composer.avatar = ''
    composer.banner = ''
    # composer.verified = 0
    composer.save()
    return JsonResponse({
        'status': 0,
        'data': {
            'callback': '/'
        }
    })


def login(request):
    return render(request, 'login.html')


def do_login(request):
    phone = request.POST.get('value')
    password = request.POST.get('password')
    composer = Composer.get_by_phone(phone)
    if not composer or composer.password != md5_pwd(phone, password):
        return JsonResponse({"status":-1,"msg":"用户名或密码错误"})
    response = JsonResponse({
        'status': 0,
        'data': {
            'callback': '/'
        }
    })
    response.set_cookie('cid', composer.cid)
    response.set_cookie('token', md5_pwd(composer.cid, settings.SECRET_KEY))
    return response


def send_code(request):
    """发送注册验证码"""
    prefix_code = request.POST.get('prefix_code')
    phone = request.POST.get('phone')
    composer = Composer.get_by_phone(phone)
    if composer:
        return JsonResponse({"status":-1025,"msg":"该手机号已注册过"})
    code = Code()
    code.phone = phone
    code.code = gen_code()
    code.ip = request.META['REMOTE_ADDR']
    code.created_at = datetime.now()
    code.save()
    send_sms_code.delay(phone, code.code)
    return JsonResponse({
        "status": 0,
        "msg": "OK",
        "data": {
            "phone": phone,
            "prefix_code": prefix_code,
        }})


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cid')
    return response


def find_password(request):
    """显示找回密码页面"""
    return render(request, 'find_password.html')


def check_send(request):
    """发送手机验证码"""
    prefix_code = request.POST.get('prefix_code')
    phone = request.POST.get('phone')
    composer = Composer.get_by_phone(phone)
    if not composer:
        return JsonResponse({"status": -1025, "msg": "该手机号未注册"})
    code = Code()
    code.phone = phone
    code.code = gen_code()
    code.ip = request.META['REMOTE_ADDR']
    code.created_at = datetime.now()
    code.save()
    send_sms_code.delay(phone, code.code)
    return JsonResponse({
        "status": 0,
        "msg": "OK",
        })


def mobile_check(request):
    """验证手机验证码"""
    phone = request.POST.get('phone')
    code = request.POST.get('code')
    prefix_code = request.POST.get('prefix_code')
    composer = Composer.get_by_phone(phone)
    if not composer:
        return JsonResponse({"status": -1025, "msg": "该手机号未注册过"})
    if not verify(phone, code):
        return JsonResponse({"status": -1, "msg": "手机验证失败"})
    response =  JsonResponse({
        "status": 0,
        "msg": "OK",
    })
    ls = str(random.randint(100000, 999999))
    response.set_cookie('laravel_session', ls,
                        expires=datetime.now() + timedelta(minutes=5))
    response.set_cookie('phone', phone, expires=datetime.now() + timedelta(minutes=5))
    cache.set(phone, ls, timeout=60*5)
    return response


def reset_pwd(request):
    """修改密码"""
    phone = request.COOKIES.get('phone')
    password =  request.POST.get('password')
    reset_password = request.POST.get('reset_password')
    if password != reset_password:
        return JsonResponse({"status":-10005,"msg":"两次输入的密码不正确"})
    if request.COOKIES.get('laravel_session') != cache.get(phone):
        return JsonResponse({
                        "status": -1,
                        "msg": "param error"
                    })
    composer = Composer.get_by_phone(phone)
    composer.password = md5_pwd(phone, password)
    composer.save()
    return JsonResponse({
        "status": 0,
        "msg": "OK",
        'data': {
            'callback': '/login/',
        }
    })