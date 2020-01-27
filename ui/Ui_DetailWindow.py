# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\lbbas\Desktop\test\webCourseQT\ui\DetailWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetailWindow(object):
    def setupUi(self, DetailWindow):
        DetailWindow.setObjectName("DetailWindow")
        DetailWindow.resize(681, 494)
        self.learn_button = QtWidgets.QPushButton(DetailWindow)
        self.learn_button.setGeometry(QtCore.QRect(280, 450, 121, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.learn_button.setFont(font)
        self.learn_button.setObjectName("learn_button")
        self.project_detail_list = QtWidgets.QTableView(DetailWindow)
        self.project_detail_list.setGeometry(QtCore.QRect(10, 60, 661, 381))
        self.project_detail_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.project_detail_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.project_detail_list.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.project_detail_list.setObjectName("project_detail_list")
        self.project_name_label = QtWidgets.QLabel(DetailWindow)
        self.project_name_label.setGeometry(QtCore.QRect(30, 20, 541, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.project_name_label.setFont(font)
        self.project_name_label.setObjectName("project_name_label")
        self.project_id_label = QtWidgets.QLabel(DetailWindow)
        self.project_id_label.setGeometry(QtCore.QRect(600, 20, 0, 0))
        self.project_id_label.setText("")
        self.project_id_label.setObjectName("project_id_label")

        self.retranslateUi(DetailWindow)
        QtCore.QMetaObject.connectSlotsByName(DetailWindow)

    def retranslateUi(self, DetailWindow):
        _translate = QtCore.QCoreApplication.translate
        DetailWindow.setWindowTitle(_translate("DetailWindow", "Dialog"))
        self.learn_button.setText(_translate("DetailWindow", "学  习"))
        self.project_name_label.setText(_translate("DetailWindow", "示例文字"))
