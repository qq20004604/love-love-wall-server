#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time


# 用户登录装饰器
def user_login_log(func):
    def wrapper(*args, **kwargs):
        if args[0].session.get('userid') is not None:
            with open('./log/user-login.log', 'a') as f:
                f.write('user:%s,login@%s,localtime:%s\n' % (
                    args[0].session.get('userid'),
                    time.time(),
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()
                                  )
                )
                        )
        return func(*args, **kwargs)

    return wrapper
