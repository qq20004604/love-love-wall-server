#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from form import Form, forms
from django.core.validators import RegexValidator


# 注册
class UserInfoForm(Form):
    id = forms.IntegerField(label='id',
                            min_value=0,
                            error_messages={
                                # 'required': '缺少id',
                                'min_value': 'id错误'
                            }
                            )
    nickname = forms.CharField(label='nickname',
                               max_length=20,
                               required=False,
                               error_messages={
                                   'max_length': '【用户昵称】长度应小于20位'
                               }
                               )
    avatar = forms.CharField(label='avatar',
                             max_length=255,
                             required=False,
                             # validators=[
                             #     RegexValidator(
                             #         r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',
                             #         '【邮箱】格式错误'
                             #     )
                             # ],
                             error_messages={
                                 'max_length': '【头像链接】长度应小于255位之间'
                             }
                             )
    qq = forms.CharField(label='qq',
                         min_length=6,
                         max_length=12,
                         required=False,
                         error_messages={
                             'max_length': 'QQ长度需要在6~12位之间',
                             'min_length': 'QQ长度需要在6~12位之间'
                         }
                         )
    wechat = forms.CharField(label='wechat',
                             max_length=50,
                             required=False,
                             error_messages={
                                 'max_length': '【微信号】长度应小于50位'
                             }
                             )
    other = forms.CharField(label='other',
                            max_length=50,
                            required=False,
                            error_messages={
                                'max_length': '【其他联系方式】长度应小于50位'
                            }
                            )
    gender = forms.CharField(label='gender',
                             max_length=5,
                             required=False,
                             error_messages={
                                 'max_length': '【性别】长度应小于5位'
                             }
                             )
    target_gender = forms.CharField(label='target_gender',
                                    max_length=5,
                                    required=False,
                                    error_messages={
                                        'max_length': '【期望对方性别】长度应小于5位'
                                    }
                                    )
    age = forms.IntegerField(label='age',
                             required=False,
                             min_value=0,
                             max_value=99,
                             error_messages={
                                 'min_value': '年龄范围应该在0~99之间',
                                 'max_value': 'max_value',
                             }
                             )
    target_age = forms.CharField(label='target_age',
                                 max_length=5,
                                 required=False,
                                 error_messages={
                                     'max_length': '【期望对方年龄】长度应小于5位'
                                 }
                                 )
    tag = forms.CharField(label='tag',
                          max_length=255,
                          required=False,
                          error_messages={
                              'max_length': '【个人标签】长度应小于255位'
                          }
                          )
    ideal = forms.CharField(label='ideal',
                            max_length=100,
                            required=False,
                            error_messages={
                                'max_length': '【理想】长度应小于100位'
                            }
                            )
    company = forms.CharField(label='company',
                              max_length=50,
                              required=False,
                              error_messages={
                                  'max_length': '【公司】长度应小于50位'
                              }
                              )
    city = forms.CharField(label='city',
                           max_length=50,
                           required=False,
                           error_messages={
                               'max_length': '【城市】长度应小于50位'
                           }
                           )
    income = forms.CharField(label='income',
                             max_length=50,
                             required=False,
                             error_messages={
                                 'max_length': '【收入】长度应小于50位'
                             }
                             )
    target_income = forms.CharField(label='target_income',
                                    max_length=50,
                                    required=False,
                                    error_messages={
                                        'max_length': '【期望收入】长度应小于50位'
                                    }
                                    )
    college = forms.CharField(label='college',
                              max_length=50,
                              required=False,
                              error_messages={
                                  'max_length': '【学校】长度应小于50位'
                              }
                              )
    profession = forms.CharField(label='profession',
                                 max_length=50,
                                 required=False,
                                 error_messages={
                                     'max_length': '【职业】长度应小于50位'
                                 }
                                 )
    summary = forms.CharField(label='summary',
                              max_length=100,
                              required=False,
                              error_messages={
                                  'max_length': '【简介】长度应小于100位'
                              }
                              )
