#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import string
import re
from .forms import RegisterForm
from response_data import get_res_json
from md5_lingling import Md5Tool
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from get_time import get_date_time
from mail.client import MailManager


def get_res(code, msg):
    return {
        'code': code,
        'msg': msg
    }


# 邮箱验证
class VerifyEmail(object):
    def __init__(self, email, vcode):
        self.email = email
        self.vcode = vcode

    def verify_email(self):
        email = self.email
        vcode = self.vcode
        # 然后去数据库找符合的数据
        # 连接数据库
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            result = mtool.run_sql([
                [
                    'SELECT * FROM verify_email WHERE email = %s and verify_key = %s and is_pass = 0',
                    [
                        email, vcode
                    ]
                ]
            ])

            # 如果查找失败，或者查不到符合的信息
            if result is False:
                return get_res(code=0, msg='激活因未知原因失败，请重试或者联系管理员。QQ：20004604，微信：qq20004604')
            if result is False or len(result) <= 0:
                return get_res(code=0, msg='验证信息不存在，请重试或者联系管理员。QQ：20004604，微信：qq20004604')

            # 查到符合的信息，则更新邮箱验证表，设置该行通过
            # 获取当前时间
            nowtime = get_date_time()
            affect_verify_email_rows = mtool.update_row(
                'UPDATE verify_email SET is_pass = 1, is_invalid = 1, last_vtime = %s WHERE email = %s and verify_key = %s',
                [
                    nowtime,
                    email,
                    vcode
                ]
            )
            if affect_verify_email_rows is False or affect_verify_email_rows is 0:
                mtool.set_uncommit()
                return get_res(code=0, msg='激活失败（0），请重试或者联系管理员。QQ：20004604，微信：qq20004604')

            # 再修改用户表，设置账号状态为启用
            affect_user_info_rows = mtool.update_row(
                'UPDATE user_info SET permission = 1 WHERE email = %s',
                [
                    email
                ]
            )
            if affect_user_info_rows is False or affect_user_info_rows is 0:
                mtool.set_uncommit()
                return get_res(code=0, msg='激活失败（1），请重试或者联系管理员。QQ：20004604，微信：qq20004604')

            return get_res(code=200, msg='激活成功')
