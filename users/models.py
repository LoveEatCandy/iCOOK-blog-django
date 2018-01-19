from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=8,verbose_name='昵称')

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=50,verbose_name='激活码')
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(max_length=10,choices=(("register","注册"),("forget","找回密码"))
                                 ,verbose_name='种类')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')
    class Meta:
        verbose_name='邮箱激活码'
        verbose_name_plural = verbose_name
