#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings

# 当前是否是webpack开发（即页面运行在webpack上）
# 假如在settings.py里，设置 DEBUG=True，则认为当前前端正在执行npm run dev（即本机环境），否则认为是线上环境
IS_ON_WEBPACK_DEVELOPMENT = True if settings.DEBUG else False
