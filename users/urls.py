#from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('signup',views.signup,name='signup'),
    path('accounts/', include('allauth.urls')),

    path('forgotpswd/',auth_views.PasswordResetView.as_view(
        template_name='users/forgotpswd.html'
    ), name = 'forgotpswd'),

    path('forgotpswd/done/',auth_views.PasswordResetDoneView.as_view(
        template_name = 'users/pswd_reset_done.html'
    ), name = 'password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'users/newpasswd.html'
    ), name = 'password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'users/reset_done.html'
    ), name = 'password_reset_complete'),


    path('logout/',LogoutView.as_view(next_page = 'home'),name = 'logout'),

]