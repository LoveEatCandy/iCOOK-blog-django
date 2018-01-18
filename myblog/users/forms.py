from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=8,max_length=20)
    passagain = forms.CharField(required=True, min_length=8, max_length=20)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
    username = forms.CharField(required=True,max_length=20)
    nick_name = forms.CharField(max_length=8)


class ForgetpwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ResetpwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=8, max_length=20)
    password2 = forms.CharField(required=True, min_length=8, max_length=20)


class CaptchaForm(forms.Form):
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})