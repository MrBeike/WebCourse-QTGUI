# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourseQT\ui\DetailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetailWindow(object):
    def setupUi(self, DetailWindow):
        DetailWindow.setObjectName("DetailWindow")
        DetailWindow.resize(681, 428)
        self.learn_button = QtWidgets.QPushButton(DetailWindow)
        self.learn_button.setGeometry(QtCore.QRect(280, 380, 121, 41))
        self.learn_button.setObjectName("learn_button")
        self.project_detail_list = QtWidgets.QTableView(DetailWindow)
        self.project_detail_list.setGeometry(QtCore.QRect(10, 20, 661, 351))
        self.project_detail_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.project_detail_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.project_detail_list.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.project_detail_list.setObjectName("project_detail_list")

        self.retranslateUi(DetailWindow)
        QtCore.QMetaObject.connectSlotsByName(DetailWindow)

    def retranslateUi(self, DetailWindow):
        _translate = QtCore.QCoreApplication.translate
        DetailWindow.setWindowTitle(_translate("DetailWindow", "Dialog"))
        self.learn_button.setText(_translate("DetailWindow", "学  习"))
