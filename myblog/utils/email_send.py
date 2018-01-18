from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from myblog.settings import EMAIL_FROM


def random_str(randomlength=10):
    str=''
    chars='ABCDEFGHIZKLMNOPQRSTUVWXYZabcdefghizklmnopqrstuvwxyz0123456789'
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,61)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code1 = random_str(30)
    code_old = EmailVerifyRecord.objects.filter(code=code1)
    while code_old:
        code1 = random_str(30)
        code_old = EmailVerifyRecord.objects.filter(code=code1)
    email_record.code = code1
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = 'iCOOK美食博客注册激活链接'
        email_body = 'iCOOK美食博客注册激活链接，请点击下面的链接激活你的账号：http://192.168.0.108:8000/user/active/{0}'.format(code1)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            return True
        else:
            return False
    elif send_type == 'forget':
        email_title = 'iCOOK美食博客密码重置链接'
        email_body = 'iCOOK美食博客密码重置链接，请点击下面的链接修改你的账号：http://192.168.0.108:8000/user/reset/{0}'.format(code1)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False


