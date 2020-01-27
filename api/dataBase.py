#!/usr/bin/python
# -*-coding:utf-8-*-
import sqlite3


'''
模块名称：用户账户管理
模块功能：利用sqllite数据库管理用户登陆信息，实现免密登陆。
功能实现：通过sql创建数据库文件保存用户信息，登录时选择“老用户登陆”则会读取该数据库文件。
'''


class DataBase:
    def __init__(self, sql):
        '''
        :param sql --a dict of sql commands.
        include  the command to create table/add data to the table as well as define the datebase filename.
        '''
        self.sql = sql
        self.conn = sqlite3.connect(self.sql['db_name'])
        self.create_table()

    def create_table(self):
        try:
            self.conn.execute(self.sql['create_table'])
            self.conn.commit()
        except:
            print('create table failed')
            return False

    def add_data(self, data):
        '''
        :param data --a dict or list.
        :return: None
        '''
        data = data
        sql = self.sql['add_data']
        sql = eval(sql)
        self.conn.execute(sql[0],sql[1])
        self.conn.commit()
        return

    def read_data(self):
        '''
        :return: data --a table like  structure list
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(self.sql['read_data'])
            data = cur.fetchall()
            self.conn.commit()
            return data
        except sqlite3.OperationalError as e:
            print("没有保存的数据",e)
            return False

    def close(self):
        try:
            self.conn.close()
        except:
            return



user_create = '''
CREATE TABLE IF NOT EXISTS USER( 
ACCOUNT  NOT NULL UNIQUE ON CONFLICT REPLACE,
 PASSWD  NOT NULL,
 NAME    NOT NULL);
'''
user_add_data = '\"REPLACE INTO USER (ACCOUNT,PASSWD,NAME) VALUES (?,?,?)\",(data["loginId"], data["passwd"], data["name"])'
user_read_data = 'select * from user'

userSQL = {'db_name': 'userinfo.db', 'create_table': user_create, 'add_data': user_add_data,
           'read_data': user_read_data}





#
# # 判断表存不存在来创建表
# def create_table(db_name):
#     conn = sqlite3.connect(db_name)
#     try:
#         create_tb_cmd = '''
#         CREATE TABLE IF NOT EXISTS USER(
#         ACCOUNT  NOT NULL UNIQUE ON CONFLICT REPLACE,
#          PASSWD  NOT NULL,
#          NAME    CHAR);
#         '''
#         # 主要就是上面的语句
#         conn.execute(create_tb_cmd)
#     except:
#         print("Create table failed")
#         return False
#
#
# def add_data(db_name, data):
#     conn = sqlite3.connect(db_name)
#     conn.execute("REPLACE INTO USER (ACCOUNT,PASSWD,NAME) VALUES (?,?,?)",
#                  (data['loginId'], data['passwd'], data['name']))
#     conn.commit()
#     conn.close()
#     return
#
#
# def read_data(db_name):
#     try:
#         conn = sqlite3.connect(db_name)
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM USER;")
#         userlistTable = PrettyTable(['序号', '用户账号', '用户名'])
#         userlist = cur.fetchall()
#         userlists = []
#         for i in range(len(userlist)):
#             userlists.append(i + 1)
#             userlists.append(userlist[i][0])
#             userlists.append(userlist[i][2])
#             userlistTable.add_row(userlists)
#             userlists.clear()
#         print(userlistTable)
#         conn.commit()
#         conn.close()
#         return userlist
#     except sqlite3.OperationalError:
#         print("没有保存的用户名和密码，请输入用户名密码")
#         return False
#
#
# def userchoose(userlist):
#     while True:
#         try:
#             choose = int(input("请输入用户序号： ")) - 1
#             webAccount = userlist[choose][0]
#             webPasswd = userlist[choose][1]
#             # 登陆时需要POST的数据
#             data = {'loginId': webAccount,
#                     'passwd': webPasswd,
#                     }
#             return data
#         except (Exception, IndexError):
#             print("输入错误")
