#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import time
from package.response_data import get_res_json
from package.decorator_csrf_setting import my_csrf_decorator
from package.decorator_user_login_log import login_intercept
from django.utils.datastructures import MultiValueDictKeyError
from session.session_manager import SM


# Create your views here.
def get_userinfo(request):
    if request.method != 'GET':
        return get_res_json(code=0, msg="请通过GET请求来进行查询")

    return get_res_json(code=200, msg="test")
