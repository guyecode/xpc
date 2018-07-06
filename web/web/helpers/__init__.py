import redis
from django.conf import settings

r = redis.Redis(host='127.0.0.1')
