#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import string
import re
import time
from .forms import SendResetPasswordMailForm, VerifyRPHrefForm
from package.response_data import get_res_json
from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
from package.get_time import get_date_time
from package.mail.client import MailManager
from .config import ResetPwSendMailVcodeLength, ResetPWSendMailExpireTimeCn, ResetPWSendMailExpireTime
from django.utils.datastructures import MultiValueDictKeyError
from package.href_str import get_href

# 重置密码的验证邮件发送间隔
PW_RWSET_MAILSEND_DURATION_SEC = 180


def get_res(code, msg):
    return {
        'code': code,
        'msg': msg
    }


# 发送密码重置邮件
# 输入：email（邮箱）
# 输出：发送一个邮件到以上邮箱，内附链接地址。（示例）http://127.0.0.1:8000/reset_password/verify?email=20004604%40qq.com&vcode=YNS20SFNQ8TJ7E2JFIS5IFNLM9NYJ9
class ResetPwSendMailManager(object):
    def __init__(self):
        pass

    # 获取请求的数据，并校验（用于发送重置密码邮件逻辑）
    def load_data(self, request):
        data = None
        # 取出数据
        if len(request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【邮箱】')
            }
        try:
            data = json.loads(request.body)
            uf = SendResetPasswordMailForm(data)
            # 验证不通过，返回错误信息
            if not uf.is_valid():
                msg = uf.get_form_error_msg()
                return {
                    'is_pass': False,
                    'res': get_res_json(code=0, msg=msg)
                }
            return {
                'is_pass': True,
                'res': data
            }
        except BaseException as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法')
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
            # 【3】【4】
            check_result = self.is_can_send(email, mtool)
            # 检查不通过，返回
            if check_result['is_pass'] is False:
                # 回滚数据库操作
                mtool.set_uncommit()
                return check_result['res']
            # 【5】【6】
            send_result = self.send(mtool, email)
            # 返回邮件发送结果
            if send_result.code is 200:
                return get_res_json(code=200, msg='密码重置邮件发送成功！')
            # 回滚数据库操作
            mtool.set_uncommit()
            return get_res_json(code=0, msg=send_result.msg)

    # 能否发送重置密码邮件
    def is_can_send(self, email, mtool):
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
            # 回滚数据库操作
            mtool.set_uncommit()
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg="该邮箱不存在，请重试或者联系管理员")
            }

        # 4、验证上一次发送重置密码邮件的时间（每次时间间隔不少于180秒）（低于这个时间，返回提示信息）
        # 尝试获取上一次发送信息
        send_result = mtool.run_sql([
            [
                'SELECT * FROM reset_pw_list WHERE email = %s and is_invalid = 0',
                [
                    email
                ]
            ]
        ])
        if send_result is False:
            # 回滚数据库操作
            mtool.set_uncommit()
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg="服务器错误(2)，请稍后再重试")
            }

        if len(send_result) > 0:
            # 说明之前有未生效重置密码的邮件。此时需要判断时间间隔
            last_send = send_result[len(send_result) - 1]
            last_send_ctime = last_send[3]
            last_sec = int(time.mktime(last_send_ctime.timetuple()))
            now_sec = int(time.time())
            sec_dur = now_sec - last_sec
            # 间隔少于指定时间，则返回错误提示信息
            if sec_dur <= PW_RWSET_MAILSEND_DURATION_SEC:
                # 回滚数据库操作
                mtool.set_uncommit()
                return {
                    'is_pass': False,
                    'res': get_res_json(code=0, msg="每次发送密码重置邮件的间隔不能少于180秒，请稍后再重新尝试发送")
                }
        return {
            'is_pass': True
        }

    # 发送邮件
    def send(self, mtool, email):
        vcode = self._get_vcode()
        # 获取当前时间
        nowtime = get_date_time()
        # 先将之前的数据设置为失效（无论之前有没有数据）
        u_result = mtool.update_row(
            'UPDATE reset_pw_list SET is_invalid=1 WHERE email=%s',
            [
                email
            ]
        )

        if u_result is False:
            # 回滚数据库操作
            mtool.set_uncommit()
            return get_res_json(code=0, msg='服务器错误(0)，请重试')

        # 数据库插入一行记录（用于之后重置密码时校验使用）
        row_id = mtool.insert_row(
            'INSERT reset_pw_list'
            '(id, email, verify_key, ctime, last_vtime, is_pass, is_invalid) VALUES'
            '(%s, %s,    %s,         %s,    %s,         0,       0)',
            [
                None,
                email,
                vcode,
                nowtime,
                nowtime
            ]
        )

        if row_id is False:
            # 回滚数据库操作
            mtool.set_uncommit()
            return get_res_json(code=0, msg='服务器错误(1)，请重试')

        # 【5】生成连接
        url = self._get_reset_url(email, vcode)
        # 此时跳转到邮件发送提示页面，提示用户点击邮箱里的链接进行验证
        send_result = self._send_resetpw_email(email, url)

        # 发送失败——》返回错误信息
        if send_result.code is not 200:
            # 回滚数据库操作
            mtool.set_uncommit()
            return get_res_json(code=0, data={
                'msg': send_result.msg
            })

        # 此时跳转到邮件发送提示页面，提示用户点击邮箱里的链接进行验证
        return get_res_json(code=200, data={
            'msg': '已发送密码重置邮件，请访问邮箱，打开邮件中的链接地址'
        })

    # 生成一个验证码
    def _get_vcode(self):
        length = ResetPwSendMailVcodeLength
        vcode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return vcode

    def _get_reset_url(self, email, vcode):
        # HOST = 'http://127.0.0.1:8000'
        # search_s = percentEncode('email=%s&vcode=%s' % (email, vcode))
        # url = '%s/reset_password/verify?%s' % (HOST, search_s)
        href = get_href('reset_password/verify', {
            'email': email,
            'vcode': vcode
        })
        return href

    # 发送验证邮件（这里可能需要再次发送验证邮件）
    def _send_resetpw_email(self, email, url):
        mm = MailManager()
        content = '重置密码请点击链接\n%s\n链接有效期为%s' % (url, ResetPWSendMailExpireTimeCn)
        # 这里是测试读取 html 内容（即发送超文本样式），也可以只发纯文本
        # with open('./content.html', 'r', encoding='utf-8') as f:
        #     content = ''.join(f.readlines()).replace(' ', '').replace('\n', '')
        mail_data = {
            'receiver': [email],
            'title': '表白墙密码重置邮件',
            'content': content,
            'account': '使用邮件服务的账号（指服务，而不是邮箱的账号）',
            'pw': '使用邮件服务的密码（指服务，而不是邮箱的密码）'
        }
        res2 = mm.send_mail(mail_data)
        # print(res2)
        return res2


# 验证密码重置链接的有效性、重置密码
class ResetPasswordManager(object):
    def __init__(self):
        pass

    # 获取请求的数据，并校验（用于重置密码链接的检验逻辑）
    def load_data_verify(self, request):
        try:
            email = request.GET['email']
        except MultiValueDictKeyError as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【邮箱】')
            }
        try:
            vcode = request.GET['vcode']
        except MultiValueDictKeyError as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【验证码】')
            }
        data = {
            'email': email,
            'vcode': vcode
        }
        uf = VerifyRPHrefForm(data)
        # 验证不通过，返回错误信息
        if not uf.is_valid():
            msg = uf.get_form_error_msg()
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg=msg)
            }
        return {
            'is_pass': True,
            'res': data
        }

    # 获取请求的数据，并校验（用于重置密码时的逻辑）
    def load_data_reset(self, request):
        data = None
        # 取出数据
        if len(request.body) is 0:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='需要【验证码】')
            }
        try:
            data = json.loads(request.body)
        except BaseException as e:
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法')
            }

        return {
            'is_pass': True,
            'res': data
        }

    # 校验验证码
    def verify_vcode(self, email, vcode):
        # 流程：
        # 1、检查邮箱、验证码是否合法；
        # 2、检查该条数据是否存在；
        # 3、检查该条数据是否在期限范围之内；
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            verify_result = self._is_vcode_correct(mtool, email, vcode)
            if verify_result['is_pass'] is True:
                return get_res(code=200)
            else:
                return get_res(code=0, msg=verify_result['res'])

    # 校验验证码是否合法
    def _is_vcode_correct(self, mtool, email, vcode):
        search_result = mtool.run_sql([
            [
                'SELECT * FROM reset_pw_list WHERE email = %s and vcode = %s and is_invaild = 0',
                [
                    email,
                    vcode
                ]
            ]
        ])
        # 查询错误或查不到内容
        if search_result is False or len(search_result) is 0:
            # 回滚数据库操作
            mtool.set_uncommit()
            return {
                'is_pass': False,
                'res': '邮箱或验证码错误'
            }
        ctime = search_result[0][3]
        last_sec = int(time.mktime(ctime.timetuple()))
        now_sec = int(time.time())
        sec_dur = now_sec - last_sec
        # 超时
        if sec_dur > ResetPWSendMailExpireTime:
            # 设置该条数据失效
            mtool.update_row(
                'UPDATE reset_pw_list SET is_invalid=1 WHERE email=%s and is_invaild=0',
                [
                    email
                ]
            )
            # 返回提示信息
            return {
                'is_pass': False,
                'res': '邮箱或验证码错误，请尝试重新发送密码重置邮件'
            }
        # 此时说明可用
        return {
            'is_pass': True
        }

    # 重置密码
    # 参数：邮箱，验证码，密码，重复密码
    def reset_pw(self, email, vcode, pw, rp_pw):
        pass

    # 密码重置
    def _pw_reset(self, email, pw):
        pass
