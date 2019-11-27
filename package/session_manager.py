#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SessionManager(object):
    def __init__(self):
        self.session_map = {}

    # 新增，key是token，value是用户信息
    def add(self, key, value):
        self.session_map[key] = value
