#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import time
from response_data import get_res_json
from decorator_csrf_setting import my_csrf_decorator
from .class_register import RegisterManager


# 打印访问人的 ip
def idlog(id):
    with open('./log/idvisit.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id
        ))


# 【喜欢】【不喜欢】日志
# 参数1：商品id int
# 参数2：喜欢或不喜欢 Boolean（该行为失败时，该值无意义）
# 参数3：该行为成功/失败 Boolean
def like_log(id, islike, success):
    with open('./log/like.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s||action=%s||success=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id,
            'like' if islike is True else 'dislike',
            'success' if success is True else 'fail'
        ))


# 注册
@my_csrf_decorator()
def register(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    rm = RegisterManager(request)
    result = rm.register()
    return result
