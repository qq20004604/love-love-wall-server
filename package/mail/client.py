#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import grpc
# import sys
# sys.path.append("../proto")
import time
from . import mail_pb2
from . import mail_pb2_grpc
from config.mail_server_config import PORT, HOST


# 记录请求发送邮件的日志
def log_mail_request(receiver, title, content, account, pw):
    with open('./log/mail_client_send.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw
        ))


# 记录请求发送邮件的日志
def log_mail_request_err(receiver, title, content, account, pw, err):
    with open('./log/mail_client_send_err.log', 'a')as f:
        f.write('time:%s||receiver:%s||title:%s||content:%s||acount:%s||pw:%s||err:%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            receiver, title, content, account, pw, err
        ))


# RPC专用类（客户端）
class MailManager(object):
    def __init__(self):
        server = '%s:%s' % (HOST, PORT)
        # 连接 rpc 服务器
        channel = grpc.insecure_channel(server)
        # 调用 rpc 服务，XxxxxStub 这个类名是固定生成的，参照 mail_pb2_grpc.py
        self.stub = mail_pb2_grpc.MailManagerServiceStub(channel)

    def send_mail(self, mail_data):
        receiver = mail_data['receiver']
        title = mail_data['title']
        content = mail_data['content']
        account = mail_data['account']
        pw = mail_data['pw']
        # print(content)
        response = None
        try:
            # s 是一个基于 dict 的实例
            s = mail_pb2.SendTextMailRequest(receiver=receiver, title=title, content=content, account=account, pw=pw)
            log_mail_request(receiver=receiver, title=title, content=content, account=account, pw=pw)
            response = self.stub.SendMail(s)
            return response
        except BaseException as e:
            log_mail_request_err(receiver=receiver, title=title, content=content, account=account, pw=pw, err=str(e))
            return {
                'code': 0,
                'msg': 'send error',
                'data': e
            }


# 测试和示例代码
if __name__ == '__main__':
    client = MailManager()
    content = ''
    # 这里是测试读取 html 内容（即发送超文本样式），也可以只发纯文本
    with open('./content.html', 'r', encoding='utf-8') as f:
        content = ''.join(f.readlines()).replace(' ', '').replace('\n', '')
    mail_data = {
        'receiver': ['test@test.com'],
        'title': '剁手器通知',
        'content': content,
        'account': '使用邮件服务的账号（指服务，而不是邮箱的账号）',
        'pw': '使用邮件服务的密码（指服务，而不是邮箱的密码）'
    }
    res2 = client.send_mail(mail_data)
    print(res2)
