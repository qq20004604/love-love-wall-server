#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql_lingling import MySQLTool
from config.mysql_options import mysql_config
import random


# 查询商品（通过id）
def search_item_byid(id=None):
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        # 目前我们获取到一个id，然后根据这个id去数据库里找一条数据，条件是【数据库数据的id >= 这个id】【只查询一条】
        items = mtool.run_sql([
            ['select * from item where pass = 1 and id <= %s ORDER BY Id DESC LIMIT 1', [id]]
        ])
        if items is False:
            return None

        # 查找这个商品有多少个【喜欢】和【不喜欢】
        likes_result = how_many_like_dislike_with_item(mtool, id)

        # print(items)
        if len(items) > 0:
            item = items[0]
            item_data = {
                'id': item[0],
                'name': item[1],
                'price': item[2],
                'reason': item[3],
                'href': item[4],
                'is_manager_push': item[6],
                'like': likes_result['like'],
                'dislike': likes_result['dislike'],
            }
            return item_data
        else:
            return None


# 查询商品（无id）
def search_item(user_ip):
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        # 先查看有多少行数据
        result = mtool.run_sql([
            ['select count(*) from item']
        ])
        # 获得有多少行数据，通常来说，当前id的索引会大于这个数字（因为可能存在空行）
        items_length = result[0][0]
        # 然后随机生成一个id
        id = random.randint(1, items_length)
        print('random item id: %s' % id)

        # 目前我们获取到一个id，然后根据这个id去数据库里找一条数据，条件是【数据库数据的id >= 这个id】【只查询一条】
        items = mtool.run_sql([
            ['select * from item where pass = 1 and id <= %s ORDER BY Id DESC LIMIT 1', [id]]
        ])
        # 如果返回结果为空，则认为没找到
        if items is False:
            return None

        # 查找这个商品有多少个【喜欢】和【不喜欢】
        likes_result = how_many_like_dislike_with_item(mtool, id)

        # print(items)
        if len(items) > 0:
            item = items[0]
            item_data = {
                'id': item[0],
                'name': item[1],
                'price': item[2],
                'reason': item[3],
                'href': item[4],
                'is_manager_push': item[6],
                'like': likes_result['like'],
                'dislike': likes_result['dislike'],
                'he_is_had_like': is_had_like(id, user_ip, mtool),
                'total_items': items_length,
                'pusher': item[7]
            }
            return item_data
        else:
            return None


# 这个人是否点过【喜欢】或者【不喜欢】
def is_had_like(id, user_ip, mtool):
    is_he_have_like = mtool.run_sql([
        [
            'SELECT * FROM item_like WHERE id = %s and user_ip like %s',
            [
                id,
                '%' + user_ip + '%'
            ]
        ]
    ])
    # 如果报错，直接返回报错。并认为没有人喜欢
    if is_he_have_like is None:
        return False
    # 如果找不到数据，显然他没点赞过
    if len(is_he_have_like) <= 0:
        return False
    else:
        # 能找到的话，说明点赞过
        return True


# 对一个商品点赞（点赞成功返回 True，否则返回 False）
# 参数 is_like 传 True 是【喜欢】， False 是【不喜欢】
def update_like_item(id, user_ip, is_like):
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        # 先查能否找到他点赞过
        he_is_had_like = is_had_like(id, user_ip, mtool)

        # 他如果点赞过，直接返回 False（更新失败，即下次点击【喜欢】或者【不喜欢】都无效）
        if he_is_had_like is True:
            return False

        # 此时说明，该人没有点赞过
        # 判断该条信息是否曾有人点赞过（需要考虑该商品是否有点赞信息）
        result = mtool.run_sql([
            ['select count(*) from item_like WHERE id = %s', [id]]
        ])
        like_length = result[0][0]
        # 1.1 情况一：该商品无点赞信息，插入【喜欢】或者【不喜欢】
        if like_length <= 0:
            insert_result = mtool.insert_row(
                'INSERT item_like (id, user_ip, like_count, dislike_count) VALUES (%s, %s, %s, %s)',
                [
                    id,
                    user_ip,
                    1 if is_like is True else 0,
                    1 if is_like is not True else 0,
                ]
            )
            # 返回不是 False，就是执行成功
            if insert_result is False:
                return False
            else:
                return True

        # 1.2 情况二：该商品存在点赞信息，则将此人的点赞信息插入该条商品中
        update_result = False
        if is_like is True:
            # 多一个【喜欢】
            update_result = mtool.update_row(
                'UPDATE item_like SET user_ip=CONCAT(user_ip, %s), like_count=like_count+1 WHERE id = %s',
                [
                    ", %s" % user_ip,
                    id
                ]
            )
        else:
            # 多一个【不喜欢】
            update_result = mtool.update_row(
                'UPDATE item_like SET user_ip=CONCAT(user_ip, %s), dislike_count=dislike_count+1 WHERE id = %s',
                [
                    ", %s" % user_ip,
                    id
                ]
            )
        if update_result is False:
            return False
        else:
            return True


# 查询一个商品有多少个【喜欢】和【不喜欢】
# 默认入参是 mtool
def how_many_like_dislike_with_item(mtool=None, id=None):
    result = mtool.run_sql([
        [
            'SELECT like_count, dislike_count FROM item_like WHERE Id = %s', [id]
        ]
    ])
    if result is False:
        return 0
    if len(result) <= 0:
        return {
            'like': 0,
            'dislike': 0
        }
    else:
        return {
            'like': result[0][0],
            'dislike': result[0][1]
        }


# 添加商品
def add_item_in_database(name, price, reason, href, pusher):
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        result = mtool.insert_row(
            'INSERT INTO item(item_name, price, reason, href, pusher) value(%s, %s, %s, %s, %s)',
            [name, price, reason, href, pusher]
        )
        return result


# 查询喜欢、不喜欢的 rank 数据
def query_likes_dislikes_ranking():
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        likes_ranking = mtool.run_sql([
            [
                'SELECT id, like_count, dislike_count FROM item_like ORDER BY like_count DESC LIMIT 10'
            ]
        ])
        dislikes_ranking = mtool.run_sql([
            [
                'SELECT id, like_count, dislike_count FROM item_like ORDER BY dislike_count DESC LIMIT 10'
            ]
        ])

        # 如果有一个请求错误，则返回空
        if likes_ranking is False or dislikes_ranking is False:
            return {
                'likes_ranking': [],
                'dislikes_ranking': []
            }

        # 先获取所有id
        id_list = []
        for like in likes_ranking:
            id_list.append(str(like[0]))
        for dislike in dislikes_ranking:
            id_list.append(str(dislike[0]))

        print("(%s)" % (', '.join(id_list)))
        # 拿到所有商品数据
        item_list = mtool.run_sql([
            [
                'SELECT id, item_name, price FROM item WHERE id in (%s)' % ', '.join(id_list),
                [
                ]
            ]
        ])

        # 做一次容错判断
        if item_list is False:
            return {
                'likes_ranking': [],
                'dislikes_ranking': []
            }

        likes_list = []
        # 将两组数据合并到一起，制造一个 【喜欢】的排行榜
        # 遍历 likes_ranking
        for like in likes_ranking:
            # 拿到当前这个的 id
            like_id = like[0]
            # 遍历 item_list，找id相同的
            for item in item_list:
                if item[0] is like_id:
                    # 组装一个dict
                    likes_list.append({
                        'id': like_id,
                        'item_name': item[1],
                        'price': item[2],
                        'like_count': like[1],
                        'dislike_count': like[2]
                    })
                    break

        dislikes_list = []
        # 同理，做一组【不喜欢】的排行榜
        for dislike in dislikes_ranking:
            # 拿到当前这个的 id
            dislike_id = dislike[0]
            # 遍历 item_list，找id相同的
            for item in item_list:
                if item[0] is dislike_id:
                    # 组装一个dict
                    dislikes_list.append({
                        'id': dislike_id,
                        'item_name': item[1],
                        'price': item[2],
                        'like_count': dislike[1],
                        'dislike_count': dislike[2]
                    })

        return {
            'likes_ranking': likes_list,
            'dislikes_ranking': dislikes_list
        }


# 根据关键字查询商品（可查商品名、描述）
def query_item_by_name_price_des(keywords):
    # 连接数据库
    with MySQLTool(host=mysql_config['host'],
                   user=mysql_config['user'],
                   password=mysql_config['pw'],
                   port=mysql_config['port'],
                   database=mysql_config['database']) as mtool:
        result = mtool.run_sql([
            [
                'SELECT * FROM item WHERE item_name LIKE %s OR reason LIKE %s',
                [
                    '%' + keywords + '%',
                    '%' + keywords + '%'
                ]
            ]
        ])
        if result is False:
            return False

        item_list = []
        for item in result:
            item_list.append({
                'id': item[0],
                'item_name': item[1],
                'price': item[2],
                'like_count': item[1],
                'dislike_count': item[2]
            })
        return item_list
