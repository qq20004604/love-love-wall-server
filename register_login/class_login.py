#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import string
from .forms import LoginForm
from libs.md5_lingling import Md5Tool
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from package.response_data import get_res_json
from package.get_time import get_date_time


def get_res(code, msg='', data={}, token=''):
    return {
        'code': code,
        'msg': msg,
        'data': data,
        'token': token
    }


class LoginManager(object):
    def __init__(self):
        self.email = ''
        self.password = ''

    def load_data(self, request):
        # 取出数据
        if len(request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【邮箱】、【密码】')
            }
        try:
            data = json.loads(request.body)
        except BaseException as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='登录数据非法')
            }

        verify_result = self._verify(data)

        # 如果验证通过
        if verify_result['is_pass'] is True:
            self.email = data.get('email')
            self.password = data.get('password')
            return {
                'is_pass': True
            }
        else:
            return verify_result

    # 校验输入内容
    def _verify(self, data):
        uf = LoginForm(data)
        # 验证不通过，返回错误信息
        if not uf.is_valid():
            msg = uf.get_form_error_msg()
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg=msg)
            }
        return {
            'is_pass': True
        }

    # 登录
    def login(self):
        # 1、从user_info表里拉取数据
        # 1.1、失败，返回并提示报错信息
        # 1.2、没有拉取到符合条件的用户、，返回并提示报错信息
        # 1.3、拉取正常，进入2
        # 2、查看该账号是否处于激活状态
        # 2.1、未激活，返回错误提示信息，并提示用户激活（走激活url）
        # 2.2、已激活，进入3
        # 3、此时说明账号密码正确，生成token，将用户信息存到token里，返回token给用户
        email = self.email
        # 密码加密
        tool = Md5Tool()
        pw = tool.get_md5(self.password)
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            select_result = mtool.run_sql([
                [
                    'SELECT * FROM user_info WHERE email = %s and pw = %s',
                    [
                        email,
                        pw
                    ]
                ]
            ])

            if select_result is False:
                return get_res(code=0, msg='服务器错误')

            if len(select_result) is 0:
                return get_res(code=0, msg='用户名/密码错误或用户不存在')

            user_info = {
                'id': select_result[0][0],
                'email': select_result[0][1],
                'permission': select_result[0][4],
                'status': select_result[0][5],
            }

            if user_info['permission'] is 0:
                return get_res(code=1, msg='邮箱未激活')

            # 获取当前时间
            nowtime = get_date_time()

            # 更新最后登录时间
            mtool.update_row(
                'UPDATE user_info SET lastlogin_time = %s WHERE id = %',
                [
                    nowtime,
                    user_info['id']
                ]
            )

            # 生成token，返回给用户
            # user_info['token'] = self.make_token()
            return get_res(code=200, data=user_info, msg='登录成功', token=self.make_token())

    def make_token(self):
        length = 20
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return token
