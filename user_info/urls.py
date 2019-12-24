#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.urls import path
from user_info import views as views

urlpatterns = [
    # 用户信息
    path('userinfo/get', views.get_userinfo),
    path('userinfo/update', views.update_userinfo),
    # 用户信息（用户获取其他用户的信息）
    # path('userinfo/user', views.other_get_userinfo),
]

urlpatterns_test = [
    # 登陆测试
    # path('test_login', views.test_login),
]
