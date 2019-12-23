#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import time
from package.response_data import get_res_json
from package.decorator_csrf_setting import my_csrf_decorator
from package.decorator_user_login_log import login_intercept
from django.utils.datastructures import MultiValueDictKeyError
from session.session_manager import SM
from .class_user_info import UserInfoManager


# 查询用户信息
@login_intercept
@my_csrf_decorator()
def get_userinfo(request):
    if request.method != 'GET':
        return get_res_json(code=0, msg="请通过GET请求来进行查询")
    # 先拿 token
    token = request.session.get('token')
    # 根据token反查用户id
    userinfo = SM.get(token)
    id = userinfo['data']['id']
    um = UserInfoManager()
    # 直接返回用户信息
    return um.get_userinfo(id)


# 更新用户信息
@login_intercept
@my_csrf_decorator()
def update_userinfo(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")
    token = request.session.get('token')
    userinfo = SM.get(token)
    id = userinfo['data']['id']
    um = UserInfoManager()
    load_result = um.load_data(request, id)
    if load_result['is_pass'] is False:
        return load_result['res']
    data = load_result['data']
    return um.update(data)
