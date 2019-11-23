#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import urllib.parse
from decorator_user_login_log import user_login_log


# 转义时间字符串，原因是时间字符串直接放在session里会导致出bug，因此需要转义一下
def percentEncode(s):
    res = urllib.parse.quote(str(s))
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    print(res)
    return res


# 登录超时时间
LOGIN_TIMEOUT = 3600


class SessionManage(object):
    def __init__(self, session):
        self.session = session
        # 当前登录的时间
        self.this_login_time = 0
        # 用户id
        self.userid = None
        # 用户名
        self.username = None
        # 用户权限
        self.permission = None
        # 用户状态
        self.status = None
        # 用户创建时间
        self.create_time = None
        # 上一次登录的时间
        self.last_login_time = None
        # 邮箱地址
        self.email = None

        # 如果用户id不为空，则这些应该都有值，从session里取值
        # 注意，这个方案并非最好的方案，有一定安全问题（因为存的东西太多了，不过为了开发方便，先这么搞）
        # 为了避免安全问题，生产环境应启用CSRF来做处理
        if self.session.get("userid") is not None:
            self.this_login_time = self.session.get("this_login_time") if self.session.get("this_login_time") else 0
            self.userid = self.session.get("userid")
            self.username = self.session.get("username")
            self.permission = self.session.get("permission")
            self.status = self.session.get("status")
            self.last_login_time = self.session.get("last_login_time")
            self.email = self.session.get("email")
            self.create_time = self.session.get("create_time")

    # 设置登录状态
    @user_login_log
    def set_login(self, userinfo_from_sql):
        [
            self.session['userid'],
            self.session['username'],
            pw,
            self.session['permission'],
            self.session['status'],
            create_time,
            last_login_time,
            self.session['email']
        ] = userinfo_from_sql

        self.session['create_time'] = percentEncode(create_time) if create_time is not None else ''
        self.session['last_login_time'] = percentEncode(last_login_time) if last_login_time is not None else ''

        self.session["this_login_time"] = time.time()
        self.this_login_time = self.session["this_login_time"]

    # 是否登录
    def is_login(self):
        if self.username is not None:
            if not self.is_login_timeout():
                return True
        return False

    # 登录是否超时
    def is_login_timeout(self):
        try:
            if time.time() - self.this_login_time > LOGIN_TIMEOUT:
                return True
            else:
                return False
        except BaseException as e:
            return True

    # 清除登录状态
    def logout(self):
        # 当前登录的时间
        self.this_login_time = 0
        # 用户id
        self.userid = None
        # 用户名
        self.username = None
        # 用户权限
        self.permission = None
        # 用户状态
        self.status = None
        # 用户创建时间
        self.create_time = None
        # 上一次登录的时间
        self.last_login_time = None
        # 邮箱地址
        self.email = None
        # 如果有登录信息，则清除
        if self.session.get('userid') is not None:
            del self.session['this_login_time']
            del self.session['userid']
            del self.session['username']
            del self.session['permission']
            del self.session['status']
            del self.session['create_time']
            del self.session['last_login_time']
            del self.session['email']

    # 获取用户信息
    def get_userinfo(self):
        d = {
            'userid': self.userid,
            'username': self.username,
            'permission': self.permission,
            'status': self.status,
            'last_login_time': self.last_login_time,
            'email': self.email,
            'create_time': self.create_time
        }
        return d


# 测试和示例代码
if __name__ == '__main__':
    pass
