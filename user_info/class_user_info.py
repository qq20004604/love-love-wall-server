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
from .config import USER_INFO_DICT


# user_info表的字典表管理器
class UserInfoDict(object):
    def __init__(self):
        self.USER_INFO_DICT = USER_INFO_DICT

    # 获取 mysql 的 update 语句。
    # 一个获取 sql 语句，一个获取 sql 参数
    def get_mysql_update_sql(self, data):
        sql = self.__get_mysql_update(data)
        val_list = self.__get_mysql_value_list(data)
        return {
            'sql': sql,
            'val_list': val_list
        }

    # 获取 sql 不含最后的值的语句（防止sql注入）
    def __get_mysql_update(self, data):
        fields_list = []
        for i in self.USER_INFO_DICT:
            k = i[0]
            if data.get(k) is not None:
                # 这个时候分为两种情况，一般字符串，或者是 list
                fields_list.append('%s=%s' % (k, '%s'))

        fields = ','.join(fields_list)
        s = 'UPDATE user_info SET %s WHERE id=%s' % (fields, data.get('id'))
        return s

    # 获取 mysql 的值
    # 参考上面，括号里的
    # 入参是用户传的值
    def __get_mysql_value_list(self, data):
        l = []
        for i in self.USER_INFO_DICT:
            k = i[0]
            v = data.get(k)
            if v is not None:
                if type(v) is list:
                    v = ','.join(v)
                l.append(v)
        return l

    # 获取 mysql 的 select 语句
    def get_mysql_select_sql(self, id):
        col_list = [
            # 'id'
        ]
        for i in self.USER_INFO_DICT:
            col_list.append(i[0])
        col_str = ','.join(col_list)

        sql = 'SELECT %s FROM user_info WHERE id = %s' % (col_str, '%s')
        return {
            'sql': sql,
            'val_list': [id]
        }

    # 这个是将 mysql 查询出来的那个 list 转为一个 dict
    def get_mysql_select_data(self, data):
        # mysql 查询到的是一个二维数组，因此先拿到这一行
        row_data = data[0]
        # 然后由于查询到的结果，是按上面 get_mysql_select_sql 里拼接的顺序返回的，因此可以获取到一个dict
        d = {
            # 'id': row_data[0]
        }
        # 新建一个数组
        for i in range(len(self.USER_INFO_DICT)):
            k = self.USER_INFO_DICT[i][0]
            d[k] = row_data[i]
        return d


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
            hidden_columns = None
            # uf.is_valid() 校验数组类型的时候非法，所以玩点骚操作
            if data['hidden_columns'] is not None:
                # 将该行数据暂时取出来
                hidden_columns = data['hidden_columns']
                # 从 data 里移除 hidden_columns 属性
                del data['hidden_columns']
            # 处理过的数据再搞到数组里
            uf = UserInfoForm(data)

            # 验证不通过，返回错误信息
            if not uf.is_valid():
                msg = uf.get_form_error_msg()
                return {
                    'is_pass': False,
                    'res': get_res_json(code=0, msg=msg)
                }
            # 再把数据加回去
            if hidden_columns is not None:
                data['hidden_columns'] = hidden_columns
            # 由于我不会用 django 的 form 校验数组，因此这里追加校验数组
            # 数组的校验，是通过 USER_INFO_DICT 的第四个元素——函数来校验的
            # 其他类型，也可以通过 这个函数 来追加校验
            # 1. 先遍历 USER_INFO_DICT
            for col_info in USER_INFO_DICT:
                # 2. 如果没有第四个参数，则继续下一个
                if len(col_info) < 4 or col_info[3] is None:
                    continue
                else:
                    # 3. 有函数的话，进行函数校验
                    if col_info[3](data[col_info[0]]) is False:
                        # 校验失败，返回报错信息
                        return {
                            'is_pass': False,
                            'res': get_res_json(code=0, msg='%s数据非法(2)' % col_info[0])
                        }

            return {
                'is_pass': True,
                'data': data
            }
        except BaseException as e:
            print(e)
            return {
                'is_pass': False,
                'res': get_res_json(code=0, msg='数据非法(1)')
            }

    # 判断数据是否存在
    def update(self, data):
        d = uid.get_mysql_update_sql(data)
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

    # 获取用户信息
    def get_userinfo(self, id):
        d = uid.get_mysql_select_sql(id)
        with MySQLTool(host=mysql_config['host'],
                       user=mysql_config['user'],
                       password=mysql_config['pw'],
                       port=mysql_config['port'],
                       database=mysql_config['database']) as mtool:
            print(d)
            select_result = mtool.run_sql([
                [
                    d['sql'],
                    d['val_list']
                ]
            ])
            if select_result is False:
                return get_res_json(code=0, msg='查询用户信息失败')
            userinfo = uid.get_mysql_select_data(select_result)
            return get_res_json(code=200, data=userinfo)
