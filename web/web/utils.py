# coding: utf-8
import random
import logging
from celery import Celery
import requests

from django.conf import settings

SMS_API_AUTH = ('api', 'key-ea9dbc7b99c8a94a3565b2c72104afb6')
logger = logging.getLogger(__name__)
app = Celery('utils', broker='redis://localhost')

@app.task
def send_sms(mobile, message):
    logger.info(u'sending sms to %s: %s' % (mobile, message))
    response = requests.post('http://sms-api.luosimao.com/v1/send.json', 
        data={'mobile': mobile, 'message': message},
        auth=SMS_API_AUTH)
    if response.ok:
        logger.info(response.text)
    else:
        logger.error('request to %s error %s' % (response.url, response.text))


def gen_code():
    return str(random.randint(100000,999999))