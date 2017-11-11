# coding:utf-8
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from web.models.composer import Composer
from web.models.code import Code
from web.utils import send_sms, gen_code

CODE_EXPIRE_SECONDS = 60 * 10


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    return render(request, 'composer.html', {'composer': composer})


def forget_pwd(request):
    return render(request, 'forget_pwd.html')


def send_sms_code(request):
    phone = request.POST.get('phone')
    ip = request.META['REMOTE_ADDR']
    code = gen_code()
    send_sms.delay(phone, code)
    Code.objects.create(code=code, phone=phone, ip=ip, created_at=datetime.now())
    data = {"status": 0, "msg": "OK", "data": {"phone": phone, "prefix_code": "+86"}}
    return JsonResponse(data, safe=False)


def check_code(request):
    phone = request.POST.get('phone')
    code = request.POST.get('code')

    co = Code.objects.filter(phone=phone, code=code).first()
    data = {"status": -1010, "msg": "校验手机验证码失败"}
    if co and (datetime.now() - co.created_at.replace(tzinfo=None)).total_seconds() < CODE_EXPIRE_SECONDS:
        data = {"status": 0, "msg": "OK"}
    return JsonResponse(data, safe=False)
