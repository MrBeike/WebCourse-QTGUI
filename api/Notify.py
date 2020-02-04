#!/usr/bin/python
# -*-coding:utf-8-*-



class Notify:
    '''
    模块名称：消息收集器
    模块功能：收集提示消息，集中展示。
    '''
    def __init__(self):
        self.message_collect = []
    
    def add(self,type,message):
        '''
        :param type 消息所属类型（所属区域）str
        :param message 加入队列的信息  str
        '''
        message_dict = {
            'type':type,
            'message': message
        }
        self.message_collect.append(message_dict)
    
    def show(self):
        message = self.message_collect.copy()
        # 清空消息队列
        self.message_collect.clear()
        return message