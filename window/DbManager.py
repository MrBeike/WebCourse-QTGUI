# -*- coding: utf-8 -*-

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot,Qt,QTimer,QFile,QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem, QSystemTrayIcon

from Ui_DbManager import *

from DataBase import DataBase,SQL

class DbManager(QDialog,Ui_DbManager):
    def __init__(self,parent=None):
        super(DbManager, self).__init__(parent)
        self.setupUi(self)
        qss_file = QFile(":/QSS/style.qss")
        qss_file.open(QFile.ReadOnly)
        qss_content= QTextStream(qss_file)
        self.qss = qss_content.readAll()
        self.setStyleSheet(self.qss)

    '''
    Table Model Defination
    '''
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

    '''
    Slot Defination
    '''
    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.user_list.currentIndex().row()
        account = self.user_list_model.index(row,1).data()
        db = DataBase(SQL)
        db.delete_data(account)
        user_result = db.read_data_formanager()
        self.user_list_model.clear()
        self.user_list_initial(user_result)