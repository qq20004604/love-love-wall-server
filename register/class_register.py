#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .forms import RegisterForm
import json
from response_data import get_res_json
from md5_lingling import Md5Tool
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from get_time import get_date_time
from session_manage import SessionManage
from config.development_config import IS_ON_WEBPACK_DEVELOPMENT


class RegisterManager(object):
    def __init__(self, request):
        self.request = request

    def register(self):
        # 取出数据
        data = json.loads(self.request.body)
        # 验证
        verify_result = self._verify(data)
        # 验证失败，返回报错信息
        if verify_result['is_pass'] is False:
            return verify_result['res']

        save_result = self._save(data)
        return save_result

    # 校验输入内容
    def _verify(self, data):
        uf = RegisterForm(data)
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

    # 保存
    def _save(self, data):
        # 拿取数据
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', None)

        # 密码加密
        tool = Md5Tool()
        md5pw = tool.get_md5(password)

        result = self._save_into_mysql(email, md5pw, phone)
        # 如果返回结果是 False，说明执行失败
        return result

    # 在数据库里进行保存
    def _save_into_mysql(self, email, md5pw, phone):
        # 连接数据库
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       database=mysql_config['database']) as mtool:
            # 查看有没有同名的用户
            result = mtool.run_sql([
                ['select (email) from user_info where name = %s', [email]]
            ])
            # 打印结果e
            print(result)
            # 判定密码是否相等
            if len(result) > 0:
                return get_res_json(code=0, msg="该邮箱已注册，请更换邮箱")

            # 获取当前时间
            nowtime = get_date_time()
            print(nowtime)

            # 插入
            row_id = mtool.insert_row(
                'INSERT user_info'
                '(id, email, pw, phone, permission, status, create_time, lastlogin_time, email) VALUES'
                '(%s, %s,   %s, %s,    3,           0,      %s,          %s,             %s)',
                [
                    None,
                    email,
                    md5pw,
                    phone,
                    nowtime,
                    nowtime,
                    email
                ]
            )

            if row_id is False:
                return get_res_json(code=0, msg='注册失败')

            # 发送激活邮件给用户
            self.send_verify_email()

            # 此时跳转到邮件发送提示页面，提示用户点击邮箱里的链接进行验证
            return get_res_json(code=200, data={
                'msg': '用户注册成功，已发送激活邮件，请访问邮箱打开激活邮件以激活账号'
            })

    # 发送验证邮件（这里可能需要再次发送验证邮件）
    def send_verify_email(self, email):
        # todo
        pass
