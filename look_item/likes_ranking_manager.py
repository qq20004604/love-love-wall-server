#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .query_database import query_likes_dislikes_ranking
import time
import threading


def likes_ranking_break_log(err):
    with open('./log/likes_ranking_break.log', 'a', encoding='utf-8')as f:
        f.write('%s||err=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            err
        ))


# 【喜欢】【不喜欢】排行管理器
class LikesRankingManager(object):
    # 初始化
    def __init__(self):
        # 【喜欢】列表（降序排列）
        self.likes_ranking = []
        # 【不喜欢】列表（降序排列）
        self.dislikes_ranking = []
        t1 = threading.Thread(target=self._eventloop, name='loop')
        t1.start()

    # 获取列表
    def get_ranking(self):
        if len(self.likes_ranking) <= 0 or len(self.dislikes_ranking) <= 0:
            self._query_ranking()
        return {
            'likes_ranking': self.likes_ranking,
            'dislikes_ranking': self.dislikes_ranking
        }

    # 向服务器请求数据，并更新
    def _query_ranking(self):
        # 先查排行列表
        result = query_likes_dislikes_ranking()
        # 此时只有 商品id、喜欢、不喜欢 这三个可用。我们还需要通过 id 去 item 表查对应的商品名
        likes_ranking = result['likes_ranking']
        dislikes_ranking = result['dislikes_ranking']

        if len(likes_ranking) > 0:
            self.likes_ranking = result['likes_ranking']
        else:
            likes_ranking_break_log('query likes_ranking is emptry')
        if len(dislikes_ranking) > 0:
            self.dislikes_ranking = result['dislikes_ranking']
        else:
            likes_ranking_break_log('query dislikes_ranking is emptry')

    # 这个是事件循环，发现有数据过期，则调用函数去redis或mysql获取最新数据
    def _eventloop(self):
        try:
            while True:
                self._query_ranking()
                time.sleep(60 * 10)  # one day in seconds
        except KeyboardInterrupt as ke:
            likes_ranking_break_log(str(ke))
            # 如果用户手动中断（比如 ctrl + c？）
            return
        except BaseException as e:
            likes_ranking_break_log(str(e))
            return


if __name__ == '__main__':
    pass
    # 注意，这个代码要执行的话，要把开始地方的
    # from .query_database import query_likes_dislikes_ranking
    # 改为
    # from query_database import query_likes_dislikes_ranking
    # import sys
    #
    # sys.path.append("..")
    # lrm = LikesRankingManager()
    # print(lrm.get_ranking())
    # time.sleep(10)
    # print(lrm.get_ranking())
