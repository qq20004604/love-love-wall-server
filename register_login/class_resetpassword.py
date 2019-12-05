#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import string
import re
from .forms import SendResetPasswordMailForm
from package.response_data import get_res_json
from libs.md5_lingling import Md5Tool
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from package.get_time import get_date_time
from package.mail.client import MailManager


def get_res(code, msg):
    return {
        'code': code,
        'msg': msg
    }


class ResetPasswordManager(object):
    def __init__(self):
        pass

    # 获取请求的数据，并校验（用于标准注册逻辑）
    def load_data(self):
        data = None
        # 取出数据
        if len(self.request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【邮箱】')
            }
        try:
            data = json.loads(self.request.body)
        except BaseException as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法')
            }

        return {
            'is_pass': True,
            'res': data
        }

    # 核心逻辑
    def send_mail(self, email):
        # 3、验证邮箱是否存在（不存在则返回，并返回提示信息）
        # 4、验证上一次发送重置密码邮件的时间（每次时间间隔不少于180秒）（低于这个时间，返回提示信息）
        # 5、生成重置密码的验证码，将验证码插入生成的链接，将链接插入生成的重置密码的邮件文本中
        # 6、发送验证邮件，并插入一条重置密码的数据，然后返回用户提示信息
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            exist_result = mtool.run_sql([
                [
                    'SELECT * FROM user_info WHERE email = %s',
                    [
                        email
                    ]
                ]
            ])

            # 3、判定邮箱是否存在
            if len(exist_result) is 0:
                return get_res_json(code=0, msg="该邮箱不存在，请重试或者联系管理员")

            # 4、验证上一次发送重置密码邮件的时间（每次时间间隔不少于180秒）（低于这个时间，返回提示信息）
            pass
