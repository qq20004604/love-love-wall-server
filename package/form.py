# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
import json


# 添加应用
class Form(forms.Form):

    def get_form_error_msg(self):
        error_json = json.loads(self.errors.as_json())
        print(error_json)
        msg = ''
        for k in error_json:
            try:
                msg = error_json[k][0]['message']
            except BaseException as e:
                print(e)
                pass
            if len(msg) > 0:
                break
        return msg
