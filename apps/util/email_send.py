__author__ = 'wzy'
__date__ = '2020/2/24 22:42'

import random

from django.core.mail import send_mail
from celery import task, shared_task

from edut_online.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def get_str(str_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    c_len = len(chars)-1
    for i in range(str_length):
        str += chars[random.randint(0, c_len)]
    return str

@shared_task
def send_email_code(email, send_type='register'):
    if send_type == 'get_code':
        act_code = get_str(4)
    else:
        act_code = get_str(16)
    em_record = EmailVerifyRecord()
    em_record.email = email
    em_record.code = act_code
    em_record.send_type = send_type
    em_record.save()

    email_title = ''
    email_body = ''

    if send_type=='register':
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(act_code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "慕学在线网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1:8000/reset/{0}".format(act_code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'get_code':
        email_title = "慕学在线邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(act_code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
