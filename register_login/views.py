#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
import time
from package.response_data import get_res_json
from package.decorator_csrf_setting import my_csrf_decorator
from package.decorator_user_login_log import login_intercept
from .class_register import RegisterManager, SendVerifyEmailAgain
from django.utils.datastructures import MultiValueDictKeyError
from .class_verify_email import VerifyEmail
from .class_login import LoginManager
from .class_resetpassword import ResetPwSendMailManager, ResetPasswordManager
from session.session_manager import SM


# 打印访问人的 id
def idlog(id):
    with open('./log/idvisit.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id
        ))


# 打印访问人的 id
def login_log(email, code):
    with open('./log/login.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s||code=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            email,
            code
        ))


# 账号激活失败的信息
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


# 账号激活
def activate_account(request):
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

    return render(request, 'verify_email.html')


# 再次发送验证邮件（用于处理没有接受到验证邮件的人）
@my_csrf_decorator()
def send_activate_email_again(request):
    if request.method != 'POST':
        return HttpResponse("请通过POST请求来进行查询")

    rm = SendVerifyEmailAgain(request)
    data = rm.load_data()
    if data['is_pass'] is False:
        return data['res']
    result = rm.send_verify_email_again(data['res'])
    return result


# 登录
@my_csrf_decorator()
def login(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    lm = LoginManager()
    # 先读取数据，读取失败返回提示信息
    load_result = lm.load_data(request)
    if load_result['is_pass'] is False:
        login_log(load_result.email, -1)
        return load_result['res']

    # 然后执行登录的逻辑，查看是否登录成功
    login_result = lm.login()
    # code不是200说明失败，返回报错信息
    # code = 0 返回默认报错信息
    if login_result['code'] is 0:
        login_log(lm.email, 0)
        return get_res_json(code=0, msg=login_result['msg'])

    # code = 1 表示 邮箱未激活，提示用户去激活邮箱
    if login_result['code'] is 1:
        # todo 这里跳转的页面应该不一样
        login_log(lm.email, 1)
        return get_res_json(code=0, msg=login_result['msg'])

    # code = 200 表示正常
    if login_result['code'] is 200:
        user_info_data = login_result['data']
        # 将token存到token管理器里
        token = login_result['token']
        SM.add(token, user_info_data)
        request.session['token'] = token
        login_log(lm.email, 200)
        return get_res_json(code=200, msg=login_result['msg'])

    # 理论上不应该执行到这里，如果执行到这里，提示错
    return get_res_json(code=2, msg="服务器错误")


# 重置密码（发送邮件）
@my_csrf_decorator()
def rp_send_mail(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    # 流程梳理：
    # 1、用户进入申请重置密码页面
    # 2、输入邮箱地址，并提交重置密码请求（进入本函数，开始进行处理）
    # 3、验证邮箱是否存在（不存在则返回，并返回提示信息）
    # 4、验证上一次发送重置密码邮件的时间（每次时间间隔不少于180秒）（低于这个时间，返回提示信息）
    # 5、生成重置密码的验证码，将验证码插入生成的链接，将链接插入生成的重置密码的邮件文本中
    # 6、发送验证邮件，并插入一条重置密码的数据，然后返回用户提示信息
    rpm = ResetPwSendMailManager()
    # 先读取数据，读取失败返回提示信息
    load_result = rpm.load_data(request)
    if load_result['is_pass'] is False:
        login_log(load_result.email, -1)
        return load_result['res']

    send_result = rpm.send_mail(load_result['res']['email'])

    return send_result


# 重置密码（验证链接）
def rp_verify(request):
    if request.method != 'GET':
        return get_res_json(code=0, msg="请通过GET请求来进行查询")

    # 流程梳理：
    # 1、用户根据连接访问重置密码页面；（进入本函数，开始进行处理）
    # 2、拿取验证码（失败则返回提示信息）；
    # 3、查找该验证码是否存在，验证码是否过期（过期时间3个小时 config.ResetPWSendMailExpireTime），该验证码是否已使用（校验失败，则返回提示信息）
    # 4、都通过后，返回重置密码的页面，内嵌验证码；
    rpm = ResetPasswordManager()
    # 先读取数据，读取失败返回提示信息
    load_result = rpm.load_data_verify(request)
    if load_result['is_pass'] is False:
        return load_result['res']
    verify_result = rpm.verify_vcode(load_result['res']['email'], load_result['res']['vcode'])
    # 验证不通过
    if verify_result['code'] is 0:
        return HttpResponse(verify_result['msg'])
    if verify_result['code'] is 200:
        return render(request, 'reset_pw.html', {
            'vcode': load_result['res']['vcode']
        })

    return get_res_json(code=200, msg="rp_verify")


# 重置密码（重置密码）
@my_csrf_decorator()
def rp_reset(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")

    # 流程梳理：
    # 1、用户根据 rp_verify() 返回的页面，输入密码，然后提交；（进入本函数，开始进行处理）
    # 2、检查密码、重复密码是否一致，检查验证码是否存在；（校验失败，则返回提示信息）
    # 3、检查验证码是否过期（校验失败，则返回提示信息）
    # 4、生成新的密码，使验证码失效，更新用户表里的密码字段的值，遍历token，如果该用户已登录，则清除登录状态，返回用户密码重置成功的提示信息；
    rpm = ResetPasswordManager()
    # 先读取数据，读取失败返回提示信息
    load_result = rpm.load_data_reset(request)
    if load_result['is_pass'] is False:
        return load_result['res']

    d = load_result['data']
    reset_result = rpm.reset_pw(d['email'], d['vcode'], d['password'])
    return reset_result


# 登录
@login_intercept
@my_csrf_decorator()
def test_login(request):
    # 没登录的话
    token = request.session.get('token')
    if token is None:
        return get_res_json(code=0, msg='你还没有登录')

    # 然后判断 SM 里该用户是否存在（登录过期判定1）
    is_exist = SM.is_exist(token)
    if is_exist is False:
        # 不存在则删除用户的token
        request.session.delete('token')
        return get_res_json(code=0, msg='未登录，或登录超时')

    # 假如存在，判定登录时间是否过期（登录过期判定2）
    is_expired = SM.is_expire(token)
    if is_expired is True:
        # 过期，则删除token
        SM.delete(token)
        return get_res_json(code=0, msg='登录超时')

    # 拿取用户信息，并返回
    user_info = SM.get(token)
    # print(token)
    return get_res_json(code=200, data=user_info)


def test_login_html(request):
    return render(request, 'login_test.html')
