from django.db import models
from datetime import datetime

from users.models import UserProfile

class Articles(models.Model):
    TYPE_CHOICES = (
        ('meet','肉类'),
        ('vegt','素食'),
        ('rice','主食'),
        ('cold','凉菜'),
        ('soup','汤'),
        ('drink','饮品'),
        ('else','其他'),
    )
    a_name=models.CharField(max_length=20,verbose_name='菜名')
    a_picture=models.ImageField(upload_to='a_img/',verbose_name='主图片')
    a_foodstuff=models.TextField(max_length=200,verbose_name='食材')
    a_time=models.DateTimeField('data published',default=datetime.now)
    a_type=models.CharField(max_length=5,choices=TYPE_CHOICES,verbose_name='分类')
    a_words=models.CharField(max_length=100,verbose_name='简介')
    a_shouchang = models.IntegerField(default=0,verbose_name='收藏量')

    class Meta:
        verbose_name='食谱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.a_name


class Steps(models.Model):
    article=models.ForeignKey(Articles,on_delete=models.CASCADE,verbose_name='食谱')
    s_text=models.TextField(max_length=100,verbose_name='步骤')
    s_picture=models.ImageField(upload_to='s_img/',null=True,blank=True,verbose_name='步骤图片')

    def __str__(self):
        return self.s_text


class UserFavorate(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
    fav_id = models.IntegerField(default=0,verbose_name='收藏的食谱ID')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    class Meta:
        verbose_name='用户收藏'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户名')
    article = models.ForeignKey(Articles,on_delete=models.CASCADE,verbose_name='食谱名')
    comment_text = models.TextField(max_length=500,verbose_name='评论内容')
    time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name='评论'
        verbose_name_plural = verbose_name


class UserReply(models.Model):
    from_who = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='from_who',verbose_name='From')
    to_who = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='to_who',verbose_name='To')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,verbose_name='评论id')
    reply_text = models.TextField(max_length=500,verbose_name='回复内容')
    time = models.DateTimeField(default=datetime.now)
    readed = models.BooleanField(default=False,verbose_name='是否已读')
    class Meta:
        verbose_name='回复'
        verbose_name_plural = verbose_name


