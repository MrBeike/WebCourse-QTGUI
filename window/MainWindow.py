# -*- coding: utf-8 -*-

# PyQt import
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot,Qt,QTimer,QFile,QTextStream,QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem, QSystemTrayIcon

# UI Defination import
from Ui_MainWindow import *

# Api import
from Login import Login
from Learn import Learn
from Regist import Regist
from DataBase import DataBase,SQL

# Window Defination import
from DetailWindow import DetailWindow
from DbManager import DbManager
from XeroxYor import XeroxYor
from NotifyWindow import NotifyWindow

# Temp import delete later
from result import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.login_status = False
        # self.login_status = True
        # 设置donate界面默认不显示
        self.donate_label.setVisible(False)
        # 设置关于界面的超链接
        self.about_label.setOpenExternalLinks(True)
        # 设置默认目录项为“用户登陆”
        self.stackedWidget.setCurrentIndex(0)
        # 加载QSS配置
        qss_file = QFile(":/QSS/style.qss")
        qss_file.open(QFile.ReadOnly)
        qss_content= QTextStream(qss_file)
        self.qss = qss_content.readAll()
        self.setStyleSheet(self.qss)
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
    Slot Defination
    '''
    # ===MainWindow===
    # List与StackDock连接
    @pyqtSlot(int)
    def on_menu_list_currentRowChanged(self, value):
        if self.login_status or value in(0,5):
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
            login = Login(username, password, rememberFla)
            login_status, s, login_message = login.login()
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
                QMessageBox.about(self,'提示',login_message)
        else:
            logout_status,s,message = login.logout()
            if logout_status:
                self.username_input.setEnabled(True)
                self.password_input.setEnabled(True)
                self.remember_check.setEnabled(True)
                self.login_status = False

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
        learn = Learn(self.s)
        row = self.project_list.currentIndex().row()
        projectId  = self.project_list_model.index(row, 4).data()
        courseLists = learn.projectDetailReader(projectId)
        notify = learn.learn(courseLists)
        notify_result = notify.show()
        self.notifywindow = NotifyWindow()
        self.notifywindow.notify_list_initial(notify_result)
        self.notifywindow.show()
        self.project_list_model.clear()
        project_result = learn.projectReader()
        self.project_list_initial(project_result)

    # 学习项目子课程按钮响应
    @pyqtSlot()
    def on_detail_button_clicked(self):
        row = self.project_list.currentIndex().row()
        projectName = self.project_list_model.index(row,0).data()
        projectId = self.project_list_model.index(row, 4).data()
        # learn = Learn(self.s)
        # project_detail_result = learn.projectDetailReader(projectId)
        # 将子窗口添加到主窗口进程中，修复闪退
        self.detailWindow = DetailWindow(projectName,projectId)
        self.detailWindow.project_detail_list_initial(project_detail_result)
        self.detailWindow.show()


    # ===course_page===
    #学习按钮响应
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
        notify = learn.learn(courseLists)
        notify_result = notify.show()
        self.notifywindow = NotifyWindow()
        self.notifywindow.notify_list_initial(notify_result)
        self.notifywindow.show()
        self.course_list_model.clear()
        course_result = learn.courseReader()
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