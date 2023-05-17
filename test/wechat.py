# -*- coding:utf-8 -*-

# Created on 2023/5/11.


import itchat


# 登录微信
itchat.auto_login(hotReload=True)

# 查找好友
friend = itchat.search_friends(name='好友昵称或备注')
if friend:
    friend = friend[0]
else:
    print("未找到该好友")
    exit()

# 发送消息
message = "你好，这是一条来自 Python 的微信消息！"
itchat.send(message, toUserName=friend['UserName'])

# 退出登录
itchat.logout()