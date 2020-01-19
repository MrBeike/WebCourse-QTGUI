#!/usr/bin/python
# -*-coding:utf-8-*-
import hashlib
import requests
import time
from dataBase import DataBase
from prettytable import PrettyTable
from bs4 import BeautifulSoup
from paramDefine import *


class Login:
    '''
    模块名称：用户登陆
    模块功能：模拟浏览器登陆远程培训系统，保存包含用户cookie的session,用于后续操作。
    @param：username: 账户 str
    @param：password: 密码 str
    @param：rememberFlag: 是否记住密码 bool
    @return: login_status: 登陆成功标志 bool
    @return：s: 成功登陆的session   requests.session()
    @return: login_message: 登陆反馈信息  str
    '''
    def __init__(self,username,password,rememberFlag):
        self.username = username
        self.password = password
        self.rememberFlag = rememberFlag

    def login():
        # 设置请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0',
                'HOST': '11.129.195.195',
                'Referer': 'http://11.129.195.195/center/cmslogin.jsp?url=11.129.195.195/sso/login_centerLogin.action',
                }
        if len(self.password) != 32:
            self.password = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
        # 登陆时需要POST的数据
        data = {'loginId': self.username,
                'passwd': self.password,
                }
        #尝试3次
        i = i + 1
        while i<3:  
            try:
                # 构造登陆请求
                s = requests.session()
                s.cookies['UC00ooIIll11'] = ''
                c = s.post(login_url, data=data, headers=headers, timeout=5)
                ctext = c.content.decode("utf-8")
                if ctext == "success":
                    page = s.get(project_url).content.decode("utf-8")
                    Soup = BeautifulSoup(page, "html.parser")
                    userName = Soup.find('a', class_="username").get_text()
                    login_message= "您以{}的身份登陆成功".format(userName)
                    if rememberFlag:
                        data['name'] = userName
                        db.add_data(data)
                    login_status = True
                elif ctext == "用户名密码不匹配，请重新输入。":
                    login_message= "用户名密码不匹配，请重试。"
                    login_status =False
                else:
                    login_message= ctext
                    login_status = False
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            except requests.exceptions.ConnectionError:
                login_message = '网络连接失败 -- 请等待1秒'
                time.sleep(1)
            except requests.exceptions.ChunkedEncodingError:
                login_message = '接收数据失败 -- 请等待1秒'
                time.sleep(1)
        return (login_status,s,login_message)
