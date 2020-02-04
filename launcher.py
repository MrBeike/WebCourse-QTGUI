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
from PyQt5.QtCore import pyqtSlot,Qt,QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem

from Ui_MainWindow import *
from Ui_DetailWindow import *
from Ui_XeroxYor import *
from Ui_DbManager import *

from Login import Login
from Learn import Learn
from Regist import Regist
from Test import Test
from Download import Download
from DataBase import DataBase,SQL

from result import *

# TODO 实验室增加注册过期课程功能
# TODO 实验室增加下载课程视频功能
# TODO 消息收集器 每个按钮结束响应
# TODO 打包方式  文件夹释放模式？

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


        # self.login_status = False
        self.login_status = True
        # 设置donate界面默认不显示
        self.donate_label.setVisible(False)
        # 设置关于界面的超链接
        self.about_label.setOpenExternalLinks(True)
        # 设置默认目录项为“用户登陆”
        self.stackedWidget.setCurrentIndex(0)
        # 加载QSS配置
        with open(r'resource\QSS.qss', 'r') as f:
            self.list_style = f.read()
        self.setStyleSheet(self.list_style)
        self.loadRememberedUser()

        # for test only Delete later {
        self.project_list_initial(project_result)
        self.course_list_initial(course_result)
        # for test only Delete later }

    def loadRememberedUser(self):
        self.username_input.clear()
        db = DataBase(SQL)
        self.userLists = db.read_data()
        usernames = [x[0] for x in self.userLists]
        self.username_input.addItems(usernames)


    '''
    Table Model Defination
    '''
    def regist_list_initial(self,search_result):
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
            self.regist_list.setColumnWidth(0,90)
            self.regist_list.setColumnWidth(1,450)
            self.regist_list.setColumnWidth(2,80)
            self.regist_list.setColumnWidth(3,0)
            self.regist_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def project_list_initial(self,project_result):
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


    def course_list_initial(self,course_result):
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
    # FIXME 未登录时 默认选中标签1 或不允许点击其他选项卡

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
                learn = Learn(s)
                project_result = learn.projectReader()
                course_result = learn.courseReader()
                self.project_list_initial(project_result)
                self.course_list_initial(course_result)
                self.login_button.setText('注  销')
                self.username_input.setEnabled(False)
                self.password_input.setEnabled(False)
                self.remember_check.setEnabled(False)
            else:
                # TODO 错误提示美化
                QMessageBox.about(self,'提示',login_message)
        else:
            logout_status,s,message = Login.logout()
            if logout_status:
                self.username_input.setEnabled(True)
                self.password_input.setEnabled(True)
                self.remember_check.setEnabled(True)
                self.login_status = False
            # TODO 注销函数未完成

    # 已保存用户名和密码同步选中
    @pyqtSlot(int)
    def on_username_input_currentIndexChanged(self, value):
        self.password_input.setText(self.userLists[value][1])

    # 账户管理按钮响应
    @pyqtSlot()
    def on_manager_button_clicked(self):
        self.dbManager = DbManager()
        db = DataBase(SQL)
        user_result = db.read_data_formanager()
        self.dbManager.user_list_initial(user_result)
        self.dbManager.show()

    # ===regist_page===
    # 搜索按钮响应
    @pyqtSlot()
    def on_search_button_clicked(self):
        # keyword = self.keyword_input.text().strip()
        # year = self.year_input.text().strip()
        # s = self.s
        # self.register = Regist(s,keyword,year)
        # search_result = self.register.search()
        self.regist_list_initial(search_result)

    # 注册按钮响应
    @pyqtSlot()
    def on_regist_button_clicked(self):
        row = self.regist_list.currentIndex().row()
        type = self.regist_list_model.index(row, 0).data()
        name = self.regist_list_model.index(row, 1).data()
        id= self.regist_list_model.index(row, 3).data()
        info = {
            'type': type,
            'name': name,
            'id': id
        }
        regist_message = self.register.regist(info)
        QMessageBox.about(self,'提示',regist_message)

    # ===project_page===
    # 学习整个项目按钮响应
    @pyqtSlot()
    def on_learnProject_button_clicked(self):
        Learn = Learn(self.s)
        row = self.project_list.currentIndex().row()
        projectId  = self.project_list_model.index(row, 4).data()
        courseLists = Learn.projectDetailReader(projectId)
        Learn.learn(courseLists)
        self.project_list_model.clear()
        project_result = Learn.projectReader()
        self.project_list_initial(project_result)

    # 学习项目子课程按钮响应
    @pyqtSlot()
    def on_detail_button_clicked(self):
        row = self.project_list.currentIndex().row()
        projectName = self.project_list_model.index(row,0).data()
        projectId = self.project_list_model.index(row, 4).data()
        # Learn = Learn(self.s)
        # project_detail_result = Learn.projectDetailReader(projectId)
        # 将子窗口添加到主窗口进程中，修复闪退
        self.detailWindow = DetailWindow(projectName,projectId)
        self.detailWindow.project_detail_list_initial(project_detail_result)
        self.detailWindow.show()


    # ===course_page===
    #学习按钮响应
    @pyqtSlot()
    def on_learnCourse_button_clicked(self):
        Learn = Learn(self.s)
        row = self.course_list.currentIndex().row()
        courseId = self.course_list_model.index(row,3).data()
        courseTime = self.course_list_model.index(row,1).data()
        # 为了函数的一致性，此处构建包含一个信息点的list [{,,,}]
        courseLists = [{
            'id':courseId,
            'time':courseTime
        }]
        Learn.learn(courseLists)
        self.course_list_model.clear()
        course_result = Learn.courseReader()
        self.course_list_initial(course_result)


    # ===lab_page===
    # TODO 存在的必要？

    # ===about_page===
    # 控制捐赠界面的开关
    @pyqtSlot(bool)
    def on_thumb_button_clicked(self, value):
        self.about_label.setHidden(value)
        self.donate_label.setVisible(value)

    # 控制隐藏界面显示
    @pyqtSlot()
    def on_xeroxyor_button_clicked(self):
        self.xeroxYor = XeroxYor()
        self.xeroxYor.show()

# 项目内课程详细信息窗体
class DetailWindow(QDialog,Ui_DetailWindow):
    def __init__(self,projectName,projectId,parent=None):
        super(DetailWindow, self).__init__(parent)
        self.setupUi(self)
        self.project_name_label.setText(str(projectName))
        self.project_id_label.setText(str(projectId))

    def project_detail_list_initial(self,project_detail_result):
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
            self.project_detail_list.setModel(self.project_detail_list_model)
        
            self.project_detail_list.setColumnWidth(0,440)
            self.project_detail_list.setColumnWidth(1,40)
            self.project_detail_list.setColumnWidth(2,70)
            self.project_detail_list.setColumnWidth(3,70)
            self.project_detail_list.setColumnWidth(4,0)
            self.project_detail_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    @pyqtSlot()
    def on_learn_button_clicked(self):
        row = self.project_detail_list.currentIndex().row()
        courseId = self.project_detail_list_model.index(row, 4).data()
        courseTime = self.course_list_model.index(row,1).data()
        # 为了函数的一致性，此处构建包含一个信息点的list [{,,,}]
        courseLists = [{
            'id':courseId,
            'time':courseTime
        }]
        Learn = Learn(self.s)
        Learn.learn(courseLists)
        self.project_detail_list_model.clear()
        
        project_detail_result = Learn.projectDetailReader(projectId)
        self.project_detail_list_initial(project_detail_result)

class DbManager(QDialog,Ui_DbManager):
    def __init__(self,parent=None):
        super(DbManager, self).__init__(parent)
        self.setupUi(self)

    def user_list_initial(self,user_result):
        self.user_list_model =QStandardItemModel()
        header =['姓名','账户名']
        self.user_list_model.setHorizontalHeaderLabels(header)
        if user_result:
            row, col = len(user_result), len(user_result[0])
            for row, datadict in enumerate(user_result):
                # datadict['loginId'],datadict['passwd'],datadict['name']
                datalist = [datadict[2],datadict[0],datadict[1]]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    value.setTextAlignment(Qt.AlignCenter)
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.user_list_model.setItem(row, col, value)
            # 添加模型到QTableView实例中
            self.user_list.setModel(self.user_list_model)
            
            # 表格栏宽、列宽调整
            self.user_list.setColumnWidth(0,100)
            self.user_list.setColumnWidth(1,300)
            self.user_list.setColumnWidth(2,0)
            self.user_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.user_list.currentIndex().row()
        account = self.user_list_model.index(row,1).data()
        db = DataBase(SQL)
        db.delete_data(account)
        user_result = db.read_data_formanager()
        self.user_list_model.clear()
        self.user_list_initial(user_result)

# 隐藏页窗体
class XeroxYor(QDialog,Ui_XeroxYor):
    def __init__(self,parent=None):
        super(XeroxYor,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.min = self.roll_text.verticalScrollBar().minimum()
        self.t = QTimer()
        self.t.timeout.connect(self.changeTxtPosition)
        self.t.start(150)

    def changeTxtPosition(self):
        self.roll_text.verticalScrollBar().setValue(self.min)
        self.min += 1
        if self.min == self.roll_text.verticalScrollBar().maximum():
            self.t.stop()
            self.destroy()

    def mousePressEvent(self, event):
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())
