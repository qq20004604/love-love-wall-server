#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import time
from response_data import get_res_json
from decorator_csrf_setting import my_csrf_decorator
from .class_register import RegisterManager
from django.utils.datastructures import MultiValueDictKeyError
from .class_verify_email import VerifyEmail
from .class_login import LoginManager


# 打印访问人的 id
def idlog(id):
    with open('./log/idvisit.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id
        ))


# 验证失败的信息
def verify_failed_log(request):
    with open('./log/verify_email_failed.log', 'a', encoding='utf-8')as f:
        # 获取用户ip
        user_ip = ''
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']

        email = ''
        vcode = ''
        try:
            email = request.GET['email']
        except MultiValueDictKeyError as e:
            pass
        try:
            vcode = request.GET['vcode']
        except MultiValueDictKeyError as e:
            pass
        f.write('%s||ip=%s||email=%s||vcode=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            user_ip,
            email,
            vcode
        ))


# 注册
@my_csrf_decorator()
def register(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    rm = RegisterManager(request)
    data = rm.load_data()
    if data['is_pass'] is False:
        return data['res']
    result = rm.register(data['res'])
    return result


# 邮箱验证
@my_csrf_decorator()
def verify_email(request):
    if request.method != 'GET':
        return HttpResponse("请通过GET请求来进行查询")
    is_error = False

    # 先尝试获取邮箱和验证码
    try:
        email = request.GET['email']
        vcode = request.GET['vcode']
    except MultiValueDictKeyError as e:
        is_error = True
        verify_failed_log(request)

    if is_error is True:
        return HttpResponse("邮箱与验证码错误")

    # 拿着邮箱和验证码，去数据库找匹配的数据
    vm = VerifyEmail(email, vcode)
    res = vm.verify_email()

    if res['code'] is 0:
        return HttpResponse(res['msg'])

    return render(request, 'verify_email.html', {
        'path': ''
    })


# 登录
@my_csrf_decorator()
def login(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    lm = LoginManager()
    # 先读取数据，读取失败返回提示信息
    load_result = lm.load_data(request)
    if load_result['is_pass'] is False:
        return load_result['res']

    # 然后执行登录的逻辑，查看是否登录成功
    login_result = lm.login()
    # code不是200说明失败，返回报错信息
    # code = 0 返回默认报错信息
    if login_result['code'] is 0:
        return get_res_json(code=0, msg=login_result['msg'])

    # code = 1 表示 邮箱未激活，提示用户去激活邮箱
    if login_result['code'] is 1:
        # todo 这里跳转的页面应该不一样
        return get_res_json(code=0, msg=login_result['msg'])

    # code = 200 表示正常
    if login_result['code'] is 200:
        user_info_data = login_result['data']
        # todo 这里添加token到session里
        # todo 测试时，返回默认提示成功数据
        return get_res_json(code=0, msg=login_result['msg'])

    # 理论上不应该执行到这里，如果执行到这里，提示错误
    return get_res_json(code=0, msg="服务器错误")
