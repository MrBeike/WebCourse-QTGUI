# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourse(QT)\ui\DetailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetailWindow(object):
    def setupUi(self, DetailWindow):
        DetailWindow.setObjectName("DetailWindow")
        DetailWindow.resize(680, 580)
        self.learn_button = QtWidgets.QPushButton(DetailWindow)
        self.learn_button.setGeometry(QtCore.QRect(280, 510, 121, 41))
        self.learn_button.setObjectName("learn_button")
        self.detail_list = QtWidgets.QTableView(DetailWindow)
        self.detail_list.setGeometry(QtCore.QRect(10, 30, 651, 461))
        self.detail_list.setObjectName("detail_list")

        self.retranslateUi(DetailWindow)
        QtCore.QMetaObject.connectSlotsByName(DetailWindow)

    def retranslateUi(self, DetailWindow):
        _translate = QtCore.QCoreApplication.translate
        DetailWindow.setWindowTitle(_translate("DetailWindow", "Dialog"))
        self.learn_button.setText(_translate("DetailWindow", "学  习"))
