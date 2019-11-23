#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from .query_database import search_item_byid, search_item, update_like_item, add_item_in_database, \
    query_item_by_name_price_des
from .likes_ranking_manager import LikesRankingManager
import time
from response_data import get_res_json
import json
from .forms import AddItemForm, SearchItemForm
from decorator_csrf_setting import my_csrf_decorator


# 打印访问人的 ip
def idlog(id):
    with open('./log/idvisit.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id
        ))


# 【喜欢】【不喜欢】日志
# 参数1：商品id int
# 参数2：喜欢或不喜欢 Boolean（该行为失败时，该值无意义）
# 参数3：该行为成功/失败 Boolean
def like_log(id, islike, success):
    with open('./log/like.log', 'a', encoding='utf-8')as f:
        f.write('%s||id=%s||action=%s||success=%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id,
            'like' if islike is True else 'dislike',
            'success' if success is True else 'fail'
        ))


# 获取/记录 访问人次
def get_visit_count():
    c = 0
    # 读取现有记录了有多少人访问
    with open('./log/visit_count.log', 'rb') as f:
        firstline = f.readline()
        # 没读取到的话，认为之前没有，本次访问设置为 1
        if len(firstline) == 0:
            c = 1
        else:
            #
            c = int(firstline) + 1

    with open('./log/visit_count.log', 'w', encoding='utf-8') as f:
        f.write(str(c))
    return c


# 获取用户 ip 地址
def get_user_ip(request):
    ip = None
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip.replace('.', '-')


lrm = LikesRankingManager()


# 访问页面时的渲染函数
# 四种情况
# 1、纯链接，无 search 字符串（默认操作，随机查询商品）
# 2、有 id：进入指定 id 查询逻辑
# 3、有 like：随机查询商品，并对 like 的商品执行【喜欢】的处理函数
# 4、有 dislike：随机查询商品，并对 dislike 的商品执行【不喜欢】的处理函数
def index(request):
    # 先尝试拿一下 id，拿到的话就是指定查询，拿不到就是随机查询
    id = None
    try:
        id = request.GET['id']
    except BaseException as e:
        # print(e)
        pass
    # 访问带 id 时，再插入
    if id is not None:
        idlog(id)
    else:
        idlog('user random id')
    # 查询有多少人访问过
    how_many_visit = get_visit_count()

    # 实例化查询控制器
    ifc = ItemFindController(request)
    # 查询，并拿到返回值
    item = ifc.find_item()
    print(item)

    if item is None:
        return render(request, 'noitems.html', {
            'how_many_visit': how_many_visit
        })
    else:
        likes_ranking = lrm.get_ranking()
        json_data = {
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'reason': item['reason'],
            'href': item['href'],
            'is_manager_push': item['is_manager_push'],
            'how_many_visit': how_many_visit,
            'like': item['like'],
            'dislike': item['dislike'],
            'he_is_had_like': item['he_is_had_like'],
            'total_items': item['total_items'],
            'likes_ranking': likes_ranking['likes_ranking'],
            'dislikes_ranking': likes_ranking['dislikes_ranking']
        }
        json_str = json.dumps(json_data)
        # return render(request, 'lookitems.html', {
        #     'data': json_str
        # })
        return render(request, 'homepage.html', {
            'data': json_str,
            'total_items': item['total_items']
        })


# 商品查找控制函数（包括 id 查询，like、dislike 查询）
class ItemFindController(object):
    def __init__(self, request):
        self.request = request

    # 查找商品
    def find_item(self):
        request = self.request
        id = None
        like_id = None
        dislike_id = None
        try:
            # 尝试获取 id 属性
            id = request.GET['id']
        except BaseException as e:
            # print(e)
            pass
        try:
            # 尝试获取 like 属性
            like_id = request.GET['like']
        except BaseException as e:
            # print(e)
            pass
        try:
            # 尝试获取 dislike 属性
            dislike_id = request.GET['dislike']
        except BaseException as e:
            # print(e)
            pass

        self._id_log(id)

        # 如果id存在，执行指定id商品查询逻辑
        if id is not None:
            search_result = search_item_byid(id)
            return search_result

        # id 不存在，则判断是否有 like 或者 dislike
        if like_id is not None or dislike_id is not None:
            # 然后先更新【喜欢】【不喜欢】
            try:
                self._like_or_not(like_id, dislike_id)
            except BaseException as e:
                print('_like_or_not error:')

        # 下来走正常的随机查询商品数据的逻辑
        # 获取用户 IP
        user_ip = get_user_ip(self.request)
        search_result = search_item(user_ip)
        return search_result

    # 打入用户查询商品日志
    def _id_log(self, id):
        # 访问带 id 时，再插入
        if id is not None:
            idlog(id)
        else:
            idlog('user random id')

    # 点赞
    def _like_or_not(self, like_id, dislike_id):
        id = None
        try:
            islike = True
            if type(like_id) is str:
                id = like_id
                islike = True
            elif type(dislike_id) is str:
                id = dislike_id
                islike = False
            else:
                id = None

            # 如果能获取到id
            if id is not None:
                # 获取用户 IP
                user_ip = get_user_ip(self.request)
                # 执行【喜欢/不喜欢】函数
                update_like_item(id, user_ip, islike)
                # 打一个日志记录一下
                like_log(id, islike, True)
            else:
                # 如果执行到这里，说明报错了，打一个日志记录一下
                like_log(None, islike, False)
        except BaseException as e:
            print(e)
            # 如果执行到这里，说明报错了，打一个日志记录一下
            like_log(id, islike, False)


# 点赞
def search_item_by_name(request):
    id = None
    try:
        id = request.GET['id']
    except BaseException as e:
        print(e)
    if id is None:
        return get_res_json(code=0, msg="id doesn't exist")
    else:
        user_ip = get_user_ip(request)
        result = update_like_item(id, user_ip)
        if result is False:
            return get_res_json(code=0, msg="id: %s，未知错误，或者你已经点过赞了，不能取消" % id)
        else:
            return get_res_json(code=200)


# 添加商品
@my_csrf_decorator()
def add_item(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行添加")
    data = json.loads(request.body)
    uf = AddItemForm(data)
    # 验证不通过，返回错误信息
    if not uf.is_valid():
        msg = uf.get_form_error_msg()
        return get_res_json(code=0, msg=msg)

    name = data.get('name')
    price = data.get('price')
    reason = data.get('reason', '')
    href = data.get('href', '')
    pusher = data.get('pusher', '')
    # 调用 database 函数插入
    result = add_item_in_database(name, price, reason, href, pusher)
    # 如果返回结果是 False，说明执行失败
    if result is False:
        return get_res_json(code=0, msg="数据库错误")
    else:
        return get_res_json(code=200, msg="添加成功，商品 id 为 %s，请等待管理员验证" % result)


# 根据关键字查询商品（可查商品名、描述）
@my_csrf_decorator()
def query_by_keywords(request):
    if request.method != 'POST':
        return get_res_json(code=0, msg="请通过POST请求来进行查询")
    data = json.loads(request.body)
    uf = SearchItemForm(data)
    # 验证不通过，返回错误信息
    if not uf.is_valid():
        msg = uf.get_form_error_msg()
        return get_res_json(code=0, msg=msg)
    keywords = data.get('keywords')
    result = query_item_by_name_price_des(keywords)
    # 如果返回结果是 False，说明执行失败
    if result is False:
        return get_res_json(code=0, msg="数据库错误")
    else:
        return get_res_json(code=200, data=result)

# 测试代码
# TEST = False
#
# if TEST is True:
#     res = query_item_by_name_price_des('好用')
#     print('-----------query_item_by_name_price_des-----------')
#     print(res)
