from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponseRedirect

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetpwdForm,ResetpwdForm
from utils.email_send import send_register_email

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        msg = request.GET.get('msg','')
        if msg == '666':
            msg ='请先登录,再进行相关操作！'
        else:
            msg = ''
        login_form = LoginForm()
        path_before = request.META.get('HTTP_REFERER', '/')
        if request.path[:5] == '/user':
            path_before = '/'
        request.session['login_from'] = path_before
        return render(request, 'users/login.html', {'login_form':login_form,'msg':msg})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    path_before = request.session['login_from']
                    del request.session['login_from']
                    cords = EmailVerifyRecord.objects.filter(email=user.email, send_type='forget')
                    if cords:
                        for cord in cords:
                            cord.delete()
                    return HttpResponseRedirect(path_before)
                else:
                    return render(request,'users/login.html',{'msg':'用户未激活邮箱','login_form':login_form})
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误','login_form':login_form})
        else:
            return render(request,'users/login.html',{'login_form':login_form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            nick_name = request.POST.get("nick_name", "***")
            user_email = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            pass_again = request.POST.get("passagain","")
            user_old1 = UserProfile.objects.filter(email=user_email)
            user_old2 = UserProfile.objects.filter(nick_name=nick_name)
            user_old3 = UserProfile.objects.filter(username=user_name)
            if user_old1:
                return render(request,'users/register.html',{
                    'email_error':'该邮箱已注册过',
                    'register_form': register_form
                })
            if user_old2:
                return render(request, 'users/register.html', {
                    'nick_error': '昵称已存在，请更换',
                    'register_form':register_form
                })
            if user_old3:
                return render(request, 'users/register.html', {
                    'name_error': '用户名已被注册，请更换',
                    'register_form':register_form
                })
            if pass_word != pass_again:
                return render(request, 'users/register.html', {
                    'password_error': '两次密码输入不相同',
                    'register_form':register_form
                })

            send_bool = send_register_email(user_email,send_type='register')
            if send_bool:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.nick_name = nick_name
                user_profile.email = user_email
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()
                return render(request,'users/sendedemail.html')
            else:
                return render(request, 'users/register.html', {
                    'email_error': '您的邮箱可能存在问题，请重试',
                    'register_form': register_form
                })
        else:
            return render(request,'users/register.html',{'register_form':register_form})



class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code,send_type='register')
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                record.delete()
            return render(request, 'users/activeok.html')
        else:
            return render(request,'users/active.html')


class ForgetpwdView(View):
    def get(self,request):
        Forgetpwd_form = ForgetpwdForm()
        return render(request, 'users/forgetpwd.html', {'Forgetpwd_form':Forgetpwd_form})

    def post(self,request):
        Forgetpwd_form = ForgetpwdForm(request.POST)
        if Forgetpwd_form.is_valid():
            user_email = request.POST.get('email','')
            user = UserProfile.objects.filter(email=user_email)
            if user:
                send_bool = send_register_email(user_email,send_type='forget')
                if send_bool:
                    return render(request, 'users/sendok.html')
                else:
                    return render(request, 'users/forgetpwd.html', {'Forgetpwd_form': Forgetpwd_form, 'msg': '您的邮箱可能存在问题，请重试'})
            else:
                return render(request, 'users/forgetpwd.html', {'Forgetpwd_form': Forgetpwd_form,'msg':'用户不存在'})
        else:
            return render(request, 'users/forgetpwd.html', {'Forgetpwd_form': Forgetpwd_form})


class ResetUserView(View):
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code,send_type='forget')
        if all_records:
            for record in all_records:
                user_email = record.email
                return render(request, 'users/password_reset.html',{'email':user_email})
        else:
            return render(request,'users/active.html')


class ModifyView(View):
    def post(self,request):
        reset_form = ResetpwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password','')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request, 'users/password_reset.html', {'email': email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,'users/resetok.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'users/password_reset.html', {'email': email, 'reset_form': reset_form})

