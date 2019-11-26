#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from session_manage import SessionManage
from response_data import get_res_json
from config.development_config import IS_ON_WEBPACK_DEVELOPMENT
from printcolor_lingling import print_red
from tools import is_static_files

# 不触发登录拦截的URL，每个元素需要是正则表达式
NOT_INTERCEPT_URLS = [
    # 注册用户
    r'^/register_login(.html)?$',
    r'^/regester_user$',
    r'^/static'
]


# 当需要重定位到登录页时，获取返回的内容
def get_redirect_login_page_response(request):
    # 末尾是html
    if len(re.findall('html$', request.path)) > 0:
        return HttpResponseRedirect('/' if not IS_ON_WEBPACK_DEVELOPMENT else '/login.html')
    else:
        # 一般的异步请求，封装code 302
        return get_res_json(code=302, msg="请登录", data={
            'redirecturl': '/login' if not IS_ON_WEBPACK_DEVELOPMENT else '/login.html'
        })


# 访问非首页，非login请求时：
#   * 未登录，则直接重定向到首页；
#   * 登录，【未超时】不做任何操作；【超时】登出并重定向到首页
# 访问首页时：
#   * 非登录，不做任何操作
#   * 登录，跳转到 /home
class not_login_to_homepage(MiddlewareMixin):
    def process_request(self, request):
        sm = SessionManage(request.session)
        if self.is_ignore(request.path):
            return

        # 如果已登录
        if sm.is_login():
            # 如果登录超时，则清除登录状态，重定向到首页
            if sm.is_login_timeout():
                print('登录超时')
                sm.logout()
                return get_redirect_login_page_response(request)
            # 如果访问登录页，则重定向到用户信息页
            if request.path == '' or request.path == '/':
                return HttpResponseRedirect('/home' if not IS_ON_WEBPACK_DEVELOPMENT else '/home.html')
        else:
            if request.path != '' and request.path != '/' and request.path != '/login':
                print_red('path:【%s】无权限登录，重定向回首页' % request.path)
                # 未登录时，重定向到首页
                return get_redirect_login_page_response(request)

        # 如果访问的url不是 / 和 /login
        # if request.path != '' and request.path != '/' and request.path != '/login':
        #     # 如果没有登录
        #     if not sm.is_login():
        #         return HttpResponseRedirect('')
        #     else:
        #         return None
        #
        # # 如果访问首页，且在登录状态，则直接进入登录
        # if request.path == '' or request.path == '/':
        #     # 如果是登录状态
        #     if sm.is_login():
        #         return HttpResponseRedirect('home')
        #     else:
        #         # 否则重定向到首页
        #         return HttpResponseRedirect('')

    # 是否被忽略
    def is_ignore(self, path):
        ingore = False
        for url in NOT_INTERCEPT_URLS:
            pattern = re.compile(url)
            # 能匹配到的话
            if pattern.search(path) is not None:
                ingore = True
        if ingore is not True:
            if is_static_files(path) is True:
                ingore = True
        return ingore


# 测试和示例代码
if __name__ == '__main__':
    pass
