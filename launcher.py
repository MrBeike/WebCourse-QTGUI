# -*- coding: utf-8 -*-

__author__ = 'xeroxYor'

import os
import sys
import os.path

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path = [os.path.join(myFolder, 'ui'),
            os.path.join(myFolder, 'resource'),
            os.path.join(myFolder, 'api')
            ] + sys.path

os.chdir(myFolder)

from Ui_MainWindow import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox
# from login import login
# from regist import Regist

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.login_status = False
        # 设置donate界面默认不显示
        self.donate_label.setVisible(False)
        with open(r'resource\QSS.qss', 'r') as f:
            self.list_style = f.read()
        self.menu_list.setStyleSheet(self.list_style)

    def project_list_initial(self):
        learn = Learn(self.s)
        project_result = learn.projectReader
        # 建立数据模型实例
        self.project_list_model = QStandardItemModel()
        # 设置列标题
        header = ['项目名称', '项目时间', '学时','完成状态','项目编号']
        self.project_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if project_result:
            row, col = len(project_result), len(project_result[0])
            for row, datadict in enumerate(project_result):
                datalist = [datadict['name'], datadict['period'],datadict['time'], datadict['status'],datadict['id']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.project_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.project_list.setModel(self.regist_list_model)
        
        self.project_list.setColumnWidth(0,300)
        self.project_list.setColumnWidth(1,300)
        self.project_list.setColumnWidth(2,20)
        self.project_list.setColumnWidth(3,30)
        self.project_list.setColumnWidth(4,30)
        self.project_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)


    def course_list_initial(self):
        learn = Learn(self.s)
        course_result = learn.courseReader
        # 建立数据模型实例
        self.course_list_model = QStandardItemModel()
        # 设置列标题
        header = ['课程名称', '学时','完成状态','课程编号']
        self.course_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if course_result:
            row, col = len(course_result), len(course_result[0])
            for row, datadict in enumerate(project_result):
                datalist = [datadict['name'],datadict['time'], datadict['status'],datadict['id']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.course_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.course_list.setModel(self.regist_list_model)
        
        self.course_list.setColumnWidth(0,350)
        self.course_list.setColumnWidth(1,20)
        self.course_list.setColumnWidth(2,30)
        self.course_list.setColumnWidth(3,280)
        self.course_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    '''
    Slots Defination
    '''
    # ===MainWindow===
    # List与StackDock连接
    @pyqtSlot(int)
    def on_menu_list_currentRowChanged(self, value):
        if (self.login_status or value == 0):
            self.stackedWidget.setCurrentIndex(value)
            
        else:
            QMessageBox.about(self, "提示", "请先登陆!")
            # TODO  美化消息提示


    # TODO 已经登录后的情况判断
    # ===login_page===
    @pyqtSlot()
    def on_login_button_clicked(self):
        username = self.username_input.currentText().strip()
        password = self.password_input.text()
        rememberFlag = self.remember_check.isChecked()
        if not username:
            QMessageBox.about(self,'提示','请输入用户名')
            return False
        if not password:
            QMessageBox.about(self,'提示','请输入密码')
            return False
        login_status, s, login_message = login(username, password, rememberFlag)
        self.statusbar.showMessage(login_message)
        if login_status:
            self.s = s
            self.login_status = login_status
            self.project_list_initial()
            self.course_list_initial()
        else:
            # TODO 错误提示美化
            QMessageBox.ablout(self,'提示',login_message)


    # ===regist_page===
    # 搜索按钮响应
    @pyqtSlot()
    def on_search_button_clicked(self):
        keyword = self.keyword_input.text().strip()
        year = self.year_input.text().strip()
        s = self.s
        self.register = Regist(s,keyword,year)
        search_result = self.register.search()
        # 建立数据模型实例
        self.regist_list_model = QStandardItemModel()
        # 设置列标题
         header = ['类型', '名称', 'ID']
        self.regist_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if search_result:
            row, col = len(search_result), len(search_result[0])
            for row, datadict in enumerate(search_result):
                datalist = [datadict['type'], datadict['name'], datadict['id']]
                # datalist = [x for x in datadict.values()]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.regist_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.regist_list.setModel(self.regist_list_model)
        
        # 表格栏宽、列宽调整
        # self.regist_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.regist_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)        
        # self.regist_list.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.regist_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.regist_list.setColumnWidth(0,50)
        self.regist_list.setColumnWidth(1,400)
        self.regist_list.setColumnWidth(2,230)
        self.regist_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    # 注册按钮响应
    @pyqtSlot()
    def on_regist_button_clicked(self):
        row = self.regist_list.currentIndex().row()
        type_index = self.regist_list_model.index(row, 0)
        name_index = self.regist_list_model.index(row, 1)
        id_index = self.regist_list_model.index(row, 2)
        type = self.regist_list_model.data(type_index)
        name = self.regist_list_model.data(name_index)
        id = self.regist_list_model.data(id_index)
        info = {
            'type': type,
            'name': name,
            'id': id
        }
        regist_message = self.register.regist(info)
        QMessageBox.about(self,'提示',regist_message)

    # ===project_page===
    # 学习整个项目按钮响应
    @pyptSlot()
    def on_learnProject_button_clicked(self):
        pass

    # 学习项目子课程按钮响应
    @pyqtSlot()
    def on_detail_button_clicked(self):
        pass

    

    # ===about_page===
    # 控制捐赠界面的开关
    @pyqtSlot(bool)
    def on_thumb_button_clicked(self, value):
        self.about_label.setHidden(value)
        self.donate_label.setVisible(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
