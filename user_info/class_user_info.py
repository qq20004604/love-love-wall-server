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


# user_info表的字典表管理器
class UserInfoDict(object):
    def __init__(self):
        # 每个list元素表示一个字段。
        # list第一个元素表示表头，list第二个元素表示他的中文
        self.USER_INFO_DICT = [
            ['nickname', '用户昵称'],
            ['avatar', '头像'],
            ['qq', 'QQ'],
            ['wechat', '微信'],
            ['other', '其他联系方式'],
            ['gender', '性别'],
            ['target_gender', '期望对方性别'],
            ['age', '期望对方年龄'],
            ['target_age', '期望对方年龄'],
            ['tag', '个人标签'],
            ['ideal', '理想'],
            ['company', '公司'],
            ['city', '所在城市'],
            ['income', '收入'],
            ['target_income', '期望对方收入'],
            ['college', '学校'],
            ['profession', '专业'],
            ['summary', '一句话介绍']
        ]

    # 获取 mysql 的 insert 语句。
    # 这里指假如有一个mysql的语句 INSERT user_info (id, nickname) VALUES (xx,xx)
    # 这里指的就是获取 "INSERT user_info (id, nickname) VALUES ()" 这部分（不包含 values 括号里面的内容，但含外面的括号）
    def get_mysql_sql(self, data):
        sql = self.__get_mysql_update(data)
        val_list = self.__get_mysql_value_list(data)
        return {
            'sql': sql,
            'val_list': val_list
        }

    def __get_mysql_update(self, data):
        fields_list = []
        for i in self.USER_INFO_DICT:
            k = i[0]
            if data.get(k) is not None:
                fields_list.append('%s=%s' % (i[0], '%s'))

        fields = ','.join(fields_list)
        s = 'UPDATE user_info SET %s WHERE id=%s' % (fields, data.get('id'))
        return s

    # 获取 mysql 的 insert 的值
    # 参考上面，括号里的
    # 入参是用户传的值
    def __get_mysql_value_list(self, data):
        l = []
        for i in self.USER_INFO_DICT:
            k = i[0]
            if data.get(k) is not None:
                l.append(data[k])
        return l


uid = UserInfoDict()


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
    def update(self, data):
        d = uid.get_mysql_sql(data)
        print(d)
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            u_result = mtool.update_row(
                d['sql'],
                d['val_list']
            )
            if u_result is not False:
                return get_res_json(code=200, msg='修改成功')
            else:
                return get_res_json(code=0, msg='修改用户信息失败')
