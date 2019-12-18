#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
from django.conf import settings


# 将一般字符串转为可以用在 href 里的字符串
def percentEncode(s):
    res = urllib.parse.quote(str(s))
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


# 输入 dict 对象，输出 href 的 search 字符串
def get_search_str(d):
    s = ''
    # 遍历k属性
    for k in d:
        # 第一个，前面没有 & 符号
        if len(s) is 0:
            s += '%s=%s' % (k, percentEncode(d[k]))
        else:
            # 后面每次拼接 & 符号
            s += '&%s=%s' % (k, percentEncode(d[k]))
    return s


# 输入HOST（可选），search字符串，关键url，返回一个 href 链接
# 示例
# href = get_href('reset_password/verify', {
#    'email': email,
#    'vcode': vcode
# })
# 返回 http://127.0.0.1:8000/reset_password/verify?email=xxx&vcode=yyy
def get_href(path, d, HOST=settings.SERVER_ORIGIN):
    search_s = get_search_str(d)
    href = '%s/%s?%s' % (HOST, path, search_s)
    return href
