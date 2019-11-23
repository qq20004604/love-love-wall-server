#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time


# 时间格式：YYYY-MM-DD hh:mm:ss
def get_date_time():
    return time.strftime("%Y-%m-%d %H:%M:%S.%ms", time.localtime())


# 时间格式：YYYY-MM-DD hh:mm:ss.xxx
def get_ms_date_time():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp
