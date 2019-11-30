#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from session.session_manager import SM
from response_data import get_res_json


def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


# 用户未登录拦截装饰器
def login_intercept(func):
    def expire_response(request):
        return get_res_json(code=-1, msg='登录过期')

    def wrapper(*args, **kwargs):
        # 先拿到token
        token = args[0].session.get('token')
        # 如果该用户登录过期、或者 token 不存在
        if SM.is_expire(token) is True:
            # 此时说明登录过期/用户不存在
            # 返回登录拦截的函数
            return expire_response(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper
