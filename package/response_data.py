#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
import json


# 获取返回数据，数据形式参考下面
# 成功的请求（符合要求，不需要报错信息的那种，比如说密码错误这种报错信息），code=200，数据在 data 里
def get_res_json(code=200, data={}, msg="success"):
    d = {
        "code": code,
        "msg": msg,
        "data": data
    }
    data = json.dumps(d)
    print(data)
    return HttpResponse(data, content_type="application/json")


# 测试和示例代码
if __name__ == '__main__':
    pass
