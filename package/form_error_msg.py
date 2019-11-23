#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


# 从form的示例中，拿取错误信息（假如验证不通过的话）
def get_form_error_msg(formdata):
    error_json = json.loads(formdata.errors.as_json())
    print(error_json)
    msg = ''
    for k in error_json:
        try:
            msg = error_json[k][0]['message']
        except BaseException as e:
            print(e)
            pass
        if len(msg) > 0:
            break
    return msg


# 测试和示例代码
if __name__ == '__main__':
    pass
