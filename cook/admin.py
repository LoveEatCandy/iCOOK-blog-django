from django.contrib import admin
from .models import Articles,Steps,Comment,UserReply,UserFavorate


class StepsInline(admin.TabularInline):
    model = Steps
    extra = 3


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息',{'fields':['a_name','a_words']}),
        ('菜品信息',{'fields':['a_foodstuff','a_picture','a_type']}),
        ('时间',{'fields':['a_time'],'classes':['collapse']})
    ]
    inlines = [StepsInline]
    list_display = ('a_name','a_type','a_time')
    list_filter = ['a_type',]


class ReplyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('回复信息', {'fields': ['from_who', 'to_who','comment','reply_text','time','readed']}),
    ]
    list_display = ('comment', 'reply_text', 'from_who','to_who')
    list_filter = ['comment', 'from_who']


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('评论信息', {'fields': ['user', 'comment_text','article','time']}),
    ]
    list_display = ('user', 'comment_text', 'article')
    list_filter = ['user', 'article']


class FavAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户收藏', {'fields': ['user', 'fav_id','add_time']}),
    ]
    list_display = ('user', 'fav_id','add_time')
    list_filter = ['user', 'fav_id']


admin.site.site_header = 'iCOOK资源管理系统'
admin.site.site_title = 'iCOOK后台管理'
admin.site.register(Articles,ArticleAdmin)
admin.site.register(UserReply,ReplyAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(UserFavorate,FavAdmin)

