#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.urls import path
from register_login import views as register_views

urlpatterns = [
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
    path('logout', register_views.logout)
]

urlpatterns_test = [
    # 登陆测试
    path('test_login', register_views.test_login),
    # 登陆测试
    path('test_login.html', register_views.test_login_html),
]
