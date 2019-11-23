#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.mysql_options import redis_config
import time
import sys
from redis_lingling import EasyRedisController


def errlog(msg):
    with open('./log/redis-err.log', 'a')as f:
        f.write('%||%s：%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            sys._getframe(1).f_code.co_name,  # 执行errlog这个函数的函数名字，即上一级函数
            msg
        ))


# 实际使用的是这个方法
class RedisWritter(EasyRedisController):
    def __init__(self, _redis_config):
        super(RedisWritter, self).__init__(_redis_config)
        # 过期时间（ms），默认是1小时，也可以手动设置
        self._expire_time = 3600
        self.list = []

    # 添加要更新的内容
    # list变量是一个list类型，list的每个元素由3个或4个元素组成，分别是：appname, key、value、过期时间（可选）
    # key = appname.key
    # value = app.value
    # expire 可填，默认是1小时（3600）
    def add_list(self, list=[]):
        self.list = list

    # 写入到redis里
    def insert_redis(self):
        try:
            for item in self.list:
                appname = item[0]
                key = item[1]
                value = item[2]
                # 设置这个key，并设置过期时间
                e_time = self._expire_time
                if len(item) == 4:
                    e_time = item[3]
                self.write('%s.%s' % (appname, key), value, e_time)
        except BaseException as e:
            err = str(e)
            errlog(err)
        finally:
            # 清空list
            self.list = []


rw = RedisWritter(redis_config)

if __name__ == '__main__':
    # 示例用法
    # 添加的结果是：key = 'key_first.key_last'   value = 'the value'
    rw.add_list([
        ['key_first', 'key_last', 'the value']
    ])
    rw.insert_redis()
