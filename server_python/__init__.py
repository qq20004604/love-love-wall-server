# import pymysql

import sys
import os
# 导入 session 管理模块
import session.session_manager

sys.path.append("libs")
sys.path.append("package")
# pymysql.install_as_MySQLdb()
if os.path.exists('log') is False:
    os.mkdir("log")

with open('./log/visit_count.log', 'a') as f:
    pass
