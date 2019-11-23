#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 红色背景
def print_red(str):
    print("\033[0;37;41m" + str + "\033[0m")


# 绿色背景
def print_green(str):
    print("\033[0;37;42m" + str + "\033[0m")


# 白色背景
def print_normal(str):
    print(str)


# 根据测试结果输出
# list形式是可变参数，至少2个参数，否则为错误
# 最后一个参数是一个字符串
# 之前的参数应当都是 True。如果至少有一个False，则为错误，其他情况为正确。
# 显示结果有两种：【1】正确，显示（字符串 + ok）【2】错误（红色背景，字符串 + Error）
def print_testresult(*list):
    length = len(list)
    if length <= 1:
        print_red(str + " ERROR !")
        return;
    str = list[length - 1]
    isCorrect = True
    # 遍历拿到索引
    for i in range(length):
        # 如果不是最后一个
        if i != length - 1:
            # 则判断他的返回值是不是 False。理论上应该都是True，如果是False则说明不符（出错了）
            if list[i] == False:
                isCorrect = False

    # 根据结果显示最后是正确还是错误，如果是错误，会有红底 和 Error 提示
    if isCorrect == True:
        print_normal(str + " OK !")
    else:
        print_red(str + " ERROR !")
