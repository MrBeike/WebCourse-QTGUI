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
        blank_data = {'loginId':'','passwd':'','name':'blank'}
        self.add_data(blank_data)

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
        data = (data["loginId"], data["passwd"], data["name"])
        self.conn.execute(self.sql['add_data'],data)
        self.conn.commit()

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

    def read_data_formanager(self):
        '''
        :return: data --a table like  structure list
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(self.sql['read_data_formanager'])
            data = cur.fetchall()
            self.conn.commit()
            return data
        except sqlite3.OperationalError as e:
            print("没有保存的数据",e)
            return False    
    
    def delete_data(self,index):
        '''
        :param index -- index to specify dataEntry(For now is account) 
        '''
        cur = self.conn.cursor()
        cur.execute(self.sql['delete_data'],(index,))
        self.conn.commit()


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
user_add_data = '''REPLACE INTO USER (ACCOUNT,PASSWD,NAME) VALUES (?,?,?)'''
user_read_data = '''SELECT * From USER ORDER BY ACCOUNT'''
user_delete_data = '''DELETE FROM USER where ACCOUNT=(?)'''
# 不显示预设的空白记录（空白记录为combox第一行显示空白所设）
user_read_data_formanager = '''SELECT * From USER WHERE NAME <>'blank' ORDER BY ACCOUNT'''

SQL = {'db_name': 'user.db', 'create_table': user_create, 'add_data': user_add_data,
           'read_data': user_read_data,'delete_data':user_delete_data,'read_data_formanager':user_read_data_formanager}
