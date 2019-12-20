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


# Create your views here.
@login_intercept
@my_csrf_decorator()
def get_userinfo(request):
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
    print(data)

    return get_res_json(code=200, msg="test")
