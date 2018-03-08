import random
from datetime import datetime
from web.models.code import Code

CODE_EXPIRE_SECONDS = 60 * 10


def gen_code():
    return str(random.randint(100000, 999999))


def verify(phone, code):
    cm = Code.objects.filter(phone=phone, code=code).first()
    if not cm:
        return False
    delay = (datetime.now() - cm.created_at.replace(tzinfo=None)).total_seconds()
    if delay > CODE_EXPIRE_SECONDS:
        return False
    return True