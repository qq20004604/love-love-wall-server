#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import time


def setlog(msg):
    with open('./log/redis-set.log', 'a')as f:
        f.write('%||%s：%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            msg
        ))


def getlog(msg):
    with open('./log/redis-get.log', 'a')as f:
        f.write('%||%s：%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            msg
        ))


# 这个是通用 redis 控制器
class EasyRedisController(object):
    # 默认设置
    def __init__(self, _redis_config):
        # 默认启动连接池模式
        pool = redis.ConnectionPool(**_redis_config)
        self.r = redis.Redis(connection_pool=pool)

    # 写入redis，默认过期时间3600秒
    # 这个和下面那个二次封装意义不大，只是加个log，虽然也可以用装饰器log，但是就酱紫吧
    def write(self, key, value, expire_time=3600):
        self.r.set(key, value, ex=expire_time)
        setlog('key=%s, value=%s, expire_time=%s' % (key, value, expire_time))

    # 读取
    def read(self, key):
        val = self.r.get(key)
        getlog('key=%s, value=%s' % (key, val))
        return val


if __name__ == '__main__':
    pass
