#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from form import Form, forms


class AddItemForm(Form):
    name = forms.CharField(label='name',
                           min_length=2,
                           max_length=40,
                           error_messages={
                               'required': '你没有填写【商品名】',
                               'max_length': '【商品名】长度需要在2~40位之间',
                               'min_length': '【商品名】长度需要在2~40位之间'
                           }
                           )
    price = forms.IntegerField(label='price',
                               min_value=0,
                               max_value=99999999,
                               error_messages={
                                   'required': '你没有填写【商品价格】',
                                   'min_value': '【商品价格】应当大于0',
                                   'max_value': '【商品价格】应当小于一个亿'
                               }
                               )
    reason = forms.CharField(label='reason',
                             min_length=None,
                             max_length=200,
                             required=False,
                             error_messages={
                                 'max_length': '【推荐原因】长度需要在200位以内',
                             }
                             )
    href = forms.CharField(label='href',
                           min_length=None,
                           max_length=240,
                           required=False,
                           error_messages={
                               'max_length': '【商品链接】长度需要在240位以内',
                           }
                           )
    pusher = forms.CharField(label='pusher',
                             min_length=None,
                             max_length=240,
                             required=False,
                             error_messages={
                                 'max_length': '【商品链接】长度需要在240位以内',
                             }
                             )


class SearchItemForm(Form):
    keywords = forms.CharField(label='keywords',
                               min_length=2,
                               max_length=40,
                               error_messages={
                                   'required': '你没有填写【查询条件】',
                                   'max_length': '【查询条件】长度需要在2~40位之间',
                                   'min_length': '【查询条件】长度需要在2~40位之间'
                               }
                               )
