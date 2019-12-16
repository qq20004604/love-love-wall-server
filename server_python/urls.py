"""server_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from register_login import api_register_manage
from register_login import views as register_views

# from login import views as login_views
# from login import

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 首页
    # path('', login_views.index),
    # 注册
    path('register', register_views.register),
    # 邮箱验证
    path('activate_account', register_views.activate_account),
    # 邮箱验证（再次发送验证邮件）
    path('send_activate_email', register_views.send_activate_email_again),
    # 登陆
    path('login', register_views.login),
    # 找回密码：发送邮件
    path('reset_password/send_mail', register_views.rp_send_mail),
    # 找回密码：验证邮件里的链接地址
    path('reset_password/verify', register_views.rp_verify),
    # 找回密码：重置密码
    path('reset_password/reset', register_views.rp_reset),
    # 找回密码：重置密码
    path('logout', register_views.logout),
    # 登陆测试
    # path('test_login', register_views.test_login),
    # 登陆测试
    # path('test_login.html', register_views.test_login_html),

    # 登录后首页
    # path('', views.index),
]
