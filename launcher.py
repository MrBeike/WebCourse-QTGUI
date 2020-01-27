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

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem

from Ui_MainWindow import *
from Ui_DetailWindow import *
from Login import Login
from Learn import Learn
from Regist import Regist
from Test import Test
from Download import Download
from result import *

# TODO 实验室增加注册过期课程功能
# TODO 保存密码用户快捷登陆
# TODO 用户登陆后界面变化
# TODO  消息收集器 每个按钮结束响应
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # self.login_status = False
        self.login_status = True
        # 设置donate界面默认不显示
        self.stackedWidget.setCurrentIndex(0)
        self.donate_label.setVisible(False)
        with open(r'resource\QSS.qss', 'r') as f:
            self.list_style = f.read()
        self.setStyleSheet(self.list_style)

        # for test only Delete later {
        self.project_list_initial()
        self.course_list_initial()
        # for test only Delete later }


    '''
    Slots Defination
    '''
    # ===MainWindow===
    # List与StackDock连接

    @pyqtSlot(int)
    def on_menu_list_currentRowChanged(self, value):
        if self.login_status or value == 0:
            self.stackedWidget.setCurrentIndex(value)  
        else:
            QMessageBox.about(self, "提示", "请先登陆!")
    # FIXME 未登录时 默认选中标签1

    # TODO 已经登录后的情况判断
    # ===login_page===
    @pyqtSlot()
    def on_login_button_clicked(self):
        if not self.login_status:
            username = self.username_input.currentText().strip()
            password = self.password_input.text()
            rememberFlag = self.remember_check.isChecked()
            if not username:
                QMessageBox.about(self,'提示','请输入用户名')
                return False
            if not password:
                QMessageBox.about(self,'提示','请输入密码')
                return False
            login_status, s, login_message = Login().login(username, password, rememberFlag)
            self.statusbar.showMessage(login_message)
            if login_status:
                self.s = s
                self.login_status = login_status
                self.project_list_initial()
                self.course_list_initial()
                self.login_button.setText('注  销')
            else:
                # TODO 错误提示美化
                QMessageBox.about(self,'提示',login_message)
        else:
            login_status,s,message = Login.logout()
            # TODO 注销函数未完成

    # ===regist_page===
    # 搜索按钮响应
    @pyqtSlot()
    def on_search_button_clicked(self):
        # keyword = self.keyword_input.text().strip()
        # year = self.year_input.text().strip()
        # s = self.s
        # self.register = Regist(s,keyword,year)
        # search_result = self.register.search()
        # 建立数据模型实例
        self.regist_list_model = QStandardItemModel()
        # 设置列标题
        header = ['类型', '名称', '注册情况','ID']
        self.regist_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if search_result:
            row, col = len(search_result), len(search_result[0])
            for row, datadict in enumerate(search_result):
                datalist = [datadict['type'], datadict['name'], datadict['status'],datadict['id']]
                # datalist = [x for x in datadict.values()]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    value.setTextAlignment(Qt.AlignCenter)
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
        self.regist_list.setColumnWidth(0,90)
        self.regist_list.setColumnWidth(1,530)
        self.regist_list.setColumnWidth(2,0)
        self.regist_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    # FIXME 注册函数有问题？
    # 注册按钮响应
    @pyqtSlot()
    def on_regist_button_clicked(self):
        row = self.regist_list.currentIndex().row()
        type = self.regist_list_model.index(row, 0).data()
        name = self.regist_list_model.index(row, 1).data()
        id= self.regist_list_model.index(row, 2).data()
        info = {
            'type': type,
            'name': name,
            'id': id
        }
        regist_message = self.register.regist(info)
        QMessageBox.about(self,'提示',regist_message)

    # ===project_page===
    def project_list_initial(self):
        # learn = Learn(self.s)
        # project_result = learn.projectReader()
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
                    value.setTextAlignment(Qt.AlignCenter)
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.project_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.project_list.setModel(self.project_list_model)
        
        self.project_list.setColumnWidth(0,370)
        self.project_list.setColumnWidth(1,150)
        self.project_list.setColumnWidth(2,40)
        self.project_list.setColumnWidth(3,60)
        self.project_list.setColumnWidth(4,0)
        self.project_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)


    def course_list_initial(self):
        # learn = Learn(self.s)
        # course_result = learn.courseReader()
        # 建立数据模型实例
        self.course_list_model = QStandardItemModel()
        # 设置列标题
        header = ['课程名称', '学时','完成状态','课程编号']
        self.course_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if course_result:
            row, col = len(course_result), len(course_result[0])
            for row, datadict in enumerate(course_result):
                datalist = [datadict['name'],datadict['time'], datadict['status'],datadict['id']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    value.setTextAlignment(Qt.AlignCenter)
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.course_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.course_list.setModel(self.course_list_model)
        
        self.course_list.setColumnWidth(0,500)
        self.course_list.setColumnWidth(1,40)
        self.course_list.setColumnWidth(2,80)
        self.course_list.setColumnWidth(3,0)
        self.course_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    # 学习整个项目按钮响应
    @pyqtSlot()
    def on_learnProject_button_clicked(self):
        learn = Learn(self.s)
        row = self.project_list.currentIndex().row()
        projectId  = self.project_list_model.index(row, 4).data()
        courseLists = learn.projectDetailReader(projectId)
        learn.learn(courseLists)
        self.project_list_initial()

    # 学习项目子课程按钮响应
    @pyqtSlot()
    def on_detail_button_clicked(self):
        # TODO 窗口初始化 传值  projectName?
        row = self.project_list.currentIndex().row()
        projectId = self.project_list_model.index(row, 4).data()
        # learn = Learn(self.s)
        # project_detail_result = learn.projectDetailReader(projectId)
        # 将子窗口添加到主窗口进程中，修复闪退
        self.detailWindow = DetailWindow()
        # 建立数据模型实例
        self.project_detail_list_model = QStandardItemModel()
        # 设置列标题
        header = ['课程名称', '学时','测试得分','是否完成','课程编号']
        self.project_detail_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if project_detail_result:
            row, col = len(project_detail_result), len(project_detail_result[0])
            for row, datadict in enumerate(project_detail_result):
                datalist = [datadict['name'],datadict['time'],datadict['score'],datadict['finished'],datadict['id']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.project_detail_list_model.setItem(row, col, value)
        # 添加模型到QTableView实例中
        self.detailWindow.project_detail_list.setModel(self.project_detail_list_model)
    
        self.detailWindow.project_detail_list.setColumnWidth(0,455)
        self.detailWindow.project_detail_list.setColumnWidth(1,40)
        self.detailWindow.project_detail_list.setColumnWidth(2,70)
        self.detailWindow.project_detail_list.setColumnWidth(3,70)
        self.detailWindow.project_detail_list.setColumnWidth(4,0)
        self.detailWindow.project_detail_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.detailWindow.show()

    # ===course_page===
    #学习按钮响应
    # FIXME 学习后视图更新失败
    @pyqtSlot()
    def on_learnCourse_button_clicked(self):
        learn = Learn(self.s)
        row = self.course_list.currentIndex().row()
        courseId = self.course_list_model.index(row,3).data()
        courseTime = self.course_list_model.index(row,1).data()
        # 为了函数的一致性，此处构建包含一个信息点的list [{,,,}]
        courseLists = [{
            'id':courseId,
            'time':courseTime
        }]
        learn.learn(courseLists)
        self.course_list_model.clear()
        self.course_list_initial()


    # ===lab_page===
    # TODO 存在的必要？

    # ===about_page===
    # 控制捐赠界面的开关
    @pyqtSlot(bool)
    def on_thumb_button_clicked(self, value):
        self.about_label.setHidden(value)
        self.donate_label.setVisible(value)

class DetailWindow(QDialog,Ui_DetailWindow):
    def __init__(self,parent=None):
        super(DetailWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())
