#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


# 当前路径是否是静态资源
def is_static_files(url):
    reg = r'\.(ico|css|js|jpg|jpeg|gif|svg|png)$'
    pattern = re.compile(reg)
    if pattern.search(url) is not None:
        return True
    else:
        return False
