# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourseQT\ui\DbManager.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DbManager(object):
    def setupUi(self, DbManager):
        DbManager.setObjectName("DbManager")
        DbManager.resize(432, 344)
        DbManager.setMinimumSize(QtCore.QSize(432, 344))
        DbManager.setMaximumSize(QtCore.QSize(432, 344))
        self.user_list = QtWidgets.QTableView(DbManager)
        self.user_list.setGeometry(QtCore.QRect(10, 50, 411, 241))
        self.user_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.user_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.user_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.user_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.user_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.user_list.setObjectName("user_list")
        self.label = QtWidgets.QLabel(DbManager)
        self.label.setGeometry(QtCore.QRect(20, 0, 161, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.delete_button = QtWidgets.QPushButton(DbManager)
        self.delete_button.setGeometry(QtCore.QRect(140, 300, 151, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")

        self.retranslateUi(DbManager)
        QtCore.QMetaObject.connectSlotsByName(DbManager)

    def retranslateUi(self, DbManager):
        _translate = QtCore.QCoreApplication.translate
        DbManager.setWindowTitle(_translate("DbManager", "已保存用户名密码管理"))
        self.label.setText(_translate("DbManager", "已记住密码的账户"))
        self.delete_button.setText(_translate("DbManager", "删  除"))
