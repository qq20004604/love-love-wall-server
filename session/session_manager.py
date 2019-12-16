#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import threading
import os

# 登录过期时间 1 天
EXPIRE_SECONDS = 60 * 60 * 24


# session 管理器
class SessionManager(object):
    def __init__(self):
        self.session_map = {}
        # 初始化时，先从文件读取session
        self.load_session()
        # 开一个新线程，执行定期清空 event_pool
        t1 = threading.Thread(target=self.loop)
        t1.setDaemon(True)
        t1.start()

    # 开一个线程，定期扫描。删除过期session，保存session到文件里
    def loop(self):
        # 先清空过期session
        self.clear_expire_session()
        # 此时我们session里都是未过期的了，将其写入文件
        self.save_session()
        # 再延迟1分钟
        time.sleep(60)

    # 新增，key是token，value是用户信息
    def add(self, key, user_auth):
        self.session_map[key] = {
            'ctime': int(time.time()),
            'data': user_auth
        }

    # 移除
    def delete(self, key):
        # 有则删除
        if key in self.session_map:
            del self.session_map[key]

    # 获取
    def get(self, key):
        if key in self.session_map:
            return self.session_map[key]
        else:
            return None

    # 判断是否过期。True过期，False正常。过期会自动删除token
    def is_expire(self, key):
        # 先判断是否存在，不存在直接认定为过期
        if self.is_exist(key) is not True:
            return True

        # 当前时间
        ntime = int(time.time())
        # 超时
        if ntime - self.session_map[key]['ctime'] > EXPIRE_SECONDS:
            return True
        else:
            return False

    # 判断某个session是否存在
    def is_exist(self, key):
        if key in self.session_map:
            return True
        else:
            return False

    # 起一个进程，定期扫描并判断session是否过期，过期则删除。将未过期的session写入文件
    def clear_expire_session(self):
        for k in self.session_map:
            # 判断是否过期，如果过期则删除
            if self.is_expire(k):
                self.delete(k)

    # 将session写入文件
    def save_session(self):
        print('-------- save session --------')
        with open('./session/session.json', 'w') as f:
            json.dump(self.session_map, f)

    # 从文件读取session
    def load_session(self):
        if os.path.isdir('session') is not True:
            os.mkdir('session')

        # 文件不存在则创建文件，但不读取直接返回
        if os.path.isfile('session/session.json') is not True:
            with open('session/session.json', 'w') as f:
                pass
            return

        with open('session/session.json', 'r') as f:
            content = f.read()
            if len(content) <= 0:
                return
            load_dict = json.loads(content)
            self.session_map = load_dict

    # 获取整个session
    def _get_sessions(self):
        return self.session_map


# 初始化，后面引用的都是他的实例
SM = SessionManager()

# 中间件，用户发起请求时调用。如果登录超时，直接返回登录超时的提示


# if __name__ == '__main__':
# print(SM.get('abc'))
# SM.add('abc', 'DDD')
# SM.save_session()
# print(SM._get_sessions())
# pass
