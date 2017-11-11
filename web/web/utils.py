# coding: utf-8
import random
import logging
from celery import Celery
import requests

SMS_API_AUTH = ('api', 'key-ea9dbc7b99c8a94a3565b2c72104afb6')
logger = logging.getLogger(__name__)
app = Celery('utils', broker='redis://localhost')


@app.task
def send_sms(mobile, code):
    message = u'尊敬的用户，您的验证码是：%s，请在10分钟内输入【千锋】' % code
    requests.post('http://sms-api.luosimao.com/v1/send.json',
                  data={'mobile': mobile, 'message': message},
                  auth=SMS_API_KEY)
    logger.info('send sms to %s: %s' % (mobile, message))


def gen_code():
    return str(random.randint(100000, 999999))
