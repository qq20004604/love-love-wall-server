#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import string
import re
import time
from .forms import UserInfoForm
from package.response_data import get_res_json
from libs.md5_lingling import Md5Tool
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from package.get_time import get_date_time
from package.mail.client import MailManager
from django.utils.datastructures import MultiValueDictKeyError
from package.href_str import get_href


class UserInfoManager(object):
    def __init__(self):
        pass

    # 获取请求的数据
    def load_data(self, request, id):
        data = None
        # 取出数据
        if len(request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法(0)')
            }
        try:
            data = json.loads(request.body)
            data['id'] = id
            uf = UserInfoForm(data)
            # 验证不通过，返回错误信息
            if not uf.is_valid():
                msg = uf.get_form_error_msg()
                return {
                    'is_pass': False,
                    'res': get_res_json(code=0, msg=msg)
                }
            return {
                'is_pass': True,
                'data': data
            }
        except BaseException as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法(1)')
            }

    # 判断数据是否存在
    def is_userinfo_exist(self):
        pass
