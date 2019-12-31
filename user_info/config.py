#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def check_hidden_columns(hide_cols):
    # 如果不是 list，则报错
    if type(hide_cols) is not list:
        return False
    # 遍历list的每个元素，不是字符串，或者是字符串，但不在 USER_INFO_DICT 里，也报错
    for col in hide_cols:
        if (type(col) is not str) or col not in USER_INFO_LIST:
            return False
        # 如果该行不允许隐藏，那么也失败
        # 获取该字段的索引
        index = USER_INFO_LIST.index(col)
        # 获取该字段所在列的信息
        col_info = USER_INFO_DICT[index]
        # 如果第三个元素的值是False（说明不允许隐藏该列），但此时该列的字段在 hide_cols 中，说明不合法
        if len(col_info) >= 3 and col_info[2] is False:
            return False

    # 验证通过，返回True
    return True


# 每个list元素表示一个字段。
# list第一个元素表示表头，
# list第二个元素表示功能描述
# list第三个元素表示能否隐藏，为False时不可以，默认可以
# list第四个元素表示校验函数，返回值为True时通过，False时失败
USER_INFO_DICT = [
    ['nickname', '用户昵称', False],
    ['avatar', '头像'],
    ['qq', 'QQ'],
    ['wechat', '微信'],
    ['other', '其他联系方式'],
    ['gender', '性别'],
    ['target_gender', '期望对方性别'],
    ['age', '期望对方年龄'],
    ['target_age', '期望对方年龄'],
    ['tag', '个人标签'],
    ['ideal', '理想'],
    ['company', '公司'],
    ['city', '所在城市'],
    ['income', '收入'],
    ['target_income', '期望对方收入'],
    ['college', '学校'],
    ['profession', '专业'],
    ['summary', '一句话介绍'],
    ['is_hidden', '是否全部隐藏不显示'],
    ['hidden_columns', '隐藏的列名，以逗号分隔', None, check_hidden_columns]
]

USER_INFO_LIST = [
    i[0] for i in USER_INFO_DICT
]
