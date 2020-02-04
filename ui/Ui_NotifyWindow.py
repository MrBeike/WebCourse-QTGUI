# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourseQT\ui\NotifyWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotifyWindow(object):
    def setupUi(self, NotifyWindow):
        NotifyWindow.setObjectName("NotifyWindow")
        NotifyWindow.resize(620, 400)
        self.notify_list = QtWidgets.QTableView(NotifyWindow)
        self.notify_list.setGeometry(QtCore.QRect(0, 0, 620, 400))
        self.notify_list.setStyleSheet("")
        self.notify_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notify_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.notify_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.notify_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.notify_list.setShowGrid(False)
        self.notify_list.setObjectName("notify_list")

        self.retranslateUi(NotifyWindow)
        QtCore.QMetaObject.connectSlotsByName(NotifyWindow)

    def retranslateUi(self, NotifyWindow):
        _translate = QtCore.QCoreApplication.translate
        NotifyWindow.setWindowTitle(_translate("NotifyWindow", "消息提示"))
import webcourse_rc
