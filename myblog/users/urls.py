from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('active/<slug:active_code>/',views.ActiveUserView.as_view(),name='active'),
    path('forgetpwd/',views.ForgetpwdView.as_view(),name='forgetpwd'),
    path('reset/<str:reset_code>/',views.ResetUserView.as_view(),name='reset'),
    path('modify/',views.ModifyView.as_view(),name='modify'),
]