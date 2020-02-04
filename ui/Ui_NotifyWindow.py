# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourseQT\ui\NotifyWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Notify(object):
    def setupUi(self, Notify):
        Notify.setObjectName("Notify")
        Notify.resize(620, 400)
        self.notify_table = QtWidgets.QTableView(Notify)
        self.notify_table.setGeometry(QtCore.QRect(0, 0, 620, 400))
        self.notify_table.setStyleSheet("")
        self.notify_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notify_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.notify_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.notify_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.notify_table.setShowGrid(False)
        self.notify_table.setObjectName("notify_table")

        self.retranslateUi(Notify)
        QtCore.QMetaObject.connectSlotsByName(Notify)

    def retranslateUi(self, Notify):
        _translate = QtCore.QCoreApplication.translate
        Notify.setWindowTitle(_translate("Notify", "消息提示"))
import webcourse_rc
