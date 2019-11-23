#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from get_time import get_ms_date_time
from tools import is_static_files
import re


def user_visit_log(msg):
    with open('./log/user_visit.log', 'a')as f:
        f.write('%s\n' % msg)


class VisitsLog(MiddlewareMixin):
    def process_response(self, request, response):
        # 如果是静态资源，则不记录
        if is_static_files(request.META['PATH_INFO']):
            return response

        # 获取用户ip
        user_ip = ''
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']
        # 用户useragent
        useragent = ''
        if 'HTTP_USER_AGENT' in request.META:
            useragent = request.META['HTTP_USER_AGENT']

        visit_path = request.META['PATH_INFO']
        nowtime = get_ms_date_time()
        status_code = response.status_code
        # 请求体内容
        request_data = request.body  # b'{"username":"12345678","password":"12345678","email":""}'
        # 去掉 password 字段后再被log
        request_data = re.sub(r'"password":"[^"]+",?', '', request_data.decode('utf-8'))
        # 日志格式:时间||路径||状态码||请求体||用户ip|用户user-agnet
        user_visit_log('%s||%s||%s||%s||%s||%s' % (nowtime, visit_path, status_code, request_data, user_ip, useragent))
        return response
