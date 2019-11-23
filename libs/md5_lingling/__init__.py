#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from printcolor_lingling import print_testresult


class Md5Tool(object):
    def __init__(self):
        pass

    # 返回字符串的 md5 编码
    def get_md5(self, str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        # 返回 md5 字符串
        return md5.hexdigest()

    # 比较字符串和md5字符串是否相等
    def is_str_md5_equal(self, str, md5str):
        result = self.get_md5(str)
        # 相等为True，不然为False
        return result == md5str

    # 返回字符串的 sha1 编码
    def get_sha1(self, str):
        md5 = hashlib.sha1()
        md5.update(str.encode('utf-8'))
        # 返回 sha1 字符串
        return md5.hexdigest()

    # 比较字符串和sha1字符串是否相等
    def is_str_sha1_equal(self, str, sha1str):
        result = self.get_sha1(str)
        # 相等为True，不然为False
        return result == sha1str


# 测试代码
if __name__ == '__main__':
    tool = Md5Tool()
    md5_1 = tool.get_md5("abcd123")
    print_testresult(md5_1 == "79cfeb94595de33b3326c06ab1c7dbda", "Md5Tool.get_md5")
    print_testresult(
        tool.is_str_md5_equal("abcd123", md5_1) == True,
        tool.is_str_md5_equal("abcd1234", md5_1) == False,
        'Md5Tool.is_str_md5_equal'
    )
    sha1_1 = tool.get_sha1("fefwefw")
    print_testresult(sha1_1 == "4bf9ae2156e1c1915e3a5da8ae3f5cd437488676", "Md5Tool.get_sha1")
    print_testresult(
        tool.is_str_sha1_equal("fefwefw", sha1_1) == True,
        tool.is_str_sha1_equal("abcd1234", sha1_1) == False,
        'Md5Tool.is_str_md5_equal'
    )
