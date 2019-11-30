#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# CSRF 装饰器，用于区分不同环境，方便开发
# 非调试模式下（DEBUG = False）启用CSRF
# 而DEBUG = True模式下，不启用CSRF，方便开发，特别是本机调试
def my_csrf_decorator():
    def fordebug_csrf_decorator(func):
        # 一个空的csrf，调试时使用
        def wrapper(*args, **kwargs):
            print('csrf close')
            return func(*args, **kwargs)

        return wrapper

    # debug状态打开的时候，返回排除csrf的装饰器。
    # DEBUG = False 时，表示启用CSRF
    if settings.DEBUG is True:
        return csrf_exempt
    else:
        return fordebug_csrf_decorator
