#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from form import Form, forms


class RegisterForm(Form):
    email = forms.CharField(label='email',
                            min_length=4,
                            max_length=60,
                            error_messages={
                                'required': '你没有填写【邮箱】',
                                'max_length': '【邮箱】长度需要在4~60位之间',
                                'min_length': '【邮箱】长度需要在4~60位之间'
                            }
                            )
    phone = forms.CharField(label='phone',
                            min_length=11,
                            max_length=11,
                            required=False,
                            error_messages={
                                'max_length': '【手机号码】长度需要11位',
                            }
                            )
    password = forms.CharField(label='password',
                               min_length=8,
                               max_length=40,
                               error_messages={
                                   'required': '你没有填写密码',
                                   'max_length': '密码长度需要在8~40位之间',
                                   'min_length': '密码长度需要在8~40位之间'
                               }
                               )
