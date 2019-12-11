#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from session.session_manager import SM
from package.response_data import get_res_json


# 被登录拦截掉的日志
def login_intercept_log(request):
    with open('log/login_intercept.log', 'a', encoding='utf-8')as f:
        # 获取用户ip
        user_ip = ''
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']
        path = request.path

        email = ''
        vcode = ''
        try:
            email = request.GET['email']
        except BaseException as e:
            pass
        try:
            vcode = request.GET['vcode']
        except BaseException as e:
            pass
        f.write('%s||ip=%s||path=%s||email=%s||vcode=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            user_ip,
            path,
            email,
            vcode
        ))


# 用户未登录拦截装饰器
def login_intercept(func):
    def expire_response(request):
        login_intercept_log(request)
        # 清除token
        request.session.delete('token')
        return get_res_json(code=-1, msg='登录过期')

    def wrapper(*args, **kwargs):
        # 先拿到token
        token = args[0].session.get('token')
        # 如果该用户登录过期、或者 token 不存在
        if SM.is_expire(token) is True:
            # 此时说明登录过期/用户不存在
            # 清除 token
            SM.delete(token)
            # 返回登录拦截的函数
            return expire_response(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper
