#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config.development_config import IS_ON_WEBPACK_DEVELOPMENT

# 这个目的是为了区分不同环境下（本机或线上），某些输出的 url 不同
# 线上环境的 host 替换 else 后面的 'http://127.0.0.1'
source_root_path = 'http://localhost:8000' if IS_ON_WEBPACK_DEVELOPMENT else ''

# 测试和示例代码
if __name__ == '__main__':
    pass
