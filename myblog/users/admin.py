from django.contrib import admin

from .models import UserProfile,EmailVerifyRecord


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户信息', {'fields': ['nick_name','username','password','email','is_superuser','is_staff','groups']}),
    ]
    list_display = ('nick_name','username', 'is_superuser', 'is_staff','email','is_active')
    list_filter = ['is_superuser','is_staff','groups','is_active']


class CordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('邮箱cord', {'fields': ['code','email','send_type','send_time']}),
    ]
    list_display = ('code','email','send_type','send_time')
    list_filter = ['email','send_type']


admin.site.register(UserProfile,UserAdmin)
admin.site.register(EmailVerifyRecord,CordAdmin)
