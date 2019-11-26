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


class RegisterManager(object):
    def __init__(self, request):
        self.request = request

    # 获取请求的数据，并校验
    def load_data(self):
        data = None
        # 取出数据
        print(self.request.body)
        if len(self.request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【邮箱】、【密码】')
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

    # 执行注册逻辑
    def register(self, data):
        # 验证
        verify_result = self._verify(data)
        # 验证失败，返回报错信息
        if verify_result['is_pass'] is False:
            return verify_result['res']

        save_result = self._save(data)
        return save_result

    # 发送验证邮件（这里可能需要再次发送验证邮件）
    def send_verify_email(self, email, vcode):
        mm = MailManager()
        href = self._get_verify_href(email, vcode)
        content = '请点击链接 %s' % href
        # 这里是测试读取 html 内容（即发送超文本样式），也可以只发纯文本
        # with open('./content.html', 'r', encoding='utf-8') as f:
        #     content = ''.join(f.readlines()).replace(' ', '').replace('\n', '')
        mail_data = {
            'receiver': ['20004604@qq.com'],
            'title': '表白墙账号注册激活邮件',
            'content': content,
            'account': '使用邮件服务的账号（指服务，而不是邮箱的账号）',
            'pw': '使用邮件服务的密码（指服务，而不是邮箱的密码）'
        }
        res2 = mm.send_mail(mail_data)
        # print(res2)
        return res2

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
        print(email, md5pw, phone)

        result = self._save_into_mysql(email, md5pw, phone)
        # 如果返回结果是 False，说明执行失败
        return result

    # 在数据库里进行保存
    def _save_into_mysql(self, email, md5pw, phone):
        vcode = None
        # 连接数据库
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            # 查看有没有同名的用户
            result = mtool.run_sql([
                ['select (email) from user_info where email = %s', [email]]
            ])
            # 打印结果e
            print(result)
            # 判定密码是否相等
            if len(result) > 0:
                return get_res_json(code=0, msg="该邮箱已注册，请更换邮箱")

            # 获取当前时间
            nowtime = get_date_time()

            # 插入
            row_id = mtool.insert_row(
                'INSERT user_info'
                '(id, email, pw, phone, permission, status, create_time, lastlogin_time) VALUES'
                '(%s, %s,   %s,  %s,    0,          0,      %s,          %s)',
                [
                    None,
                    email,
                    md5pw,
                    phone,
                    nowtime,
                    nowtime
                ]
            )

            if row_id is False:
                return get_res_json(code=0, msg='注册失败')

            vcode = self._get_verify_code()
            self._insert_info_into_verify(mtool, email, vcode)

        # 发送激活邮件给用户
        send_result = self.send_verify_email(email, vcode)

        # 发送失败——》返回错误信息
        if send_result.code is not 200:
            return get_res_json(code=200, data={
                'msg': send_result.msg
            })

        # 此时跳转到邮件发送提示页面，提示用户点击邮箱里的链接进行验证
        return get_res_json(code=200, data={
            'msg': '用户注册成功，已发送激活邮件，请访问邮箱打开激活邮件以激活账号'
        })

    # 插入一条邮箱验证信息
    def _insert_info_into_verify(self, mtool, email, vcode):
        # 1、先检查该邮箱是否已有一条验证数据，有则使之失效
        # 2、插入一条该邮箱的验证信息
        # 1、使之失效
        mtool.update_row(
            'UPDATE verify_email SET is_invalid=1 WHERE email=%s',
            [
                email
            ]
        )
        # 获取当前时间
        nowtime = get_date_time()
        # 2、插入一条验证信息
        mtool.insert_row(
            'INSERT verify_email '
            '(id, email, verify_key, ctime, last_vtime, is_pass, is_invalid) VALUES'
            '(%s, %s,    %s,         %s,    %s,         %s,      %s)',
            [
                None,
                email,
                vcode,
                nowtime,
                None,
                None,
                None
            ]
        )

    # 生成一个验证码
    def _get_verify_code(self):
        length = 30
        vcode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return vcode

    # 返回验证链接
    def _get_verify_href(self, email, vcode):
        host = '127.0.0.1:8000'
        href = '%s/verify_email?email=%s&vcode=%s' % (host, email, vcode)
        return href
