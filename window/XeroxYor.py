# -*- coding: utf-8 -*-

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot,Qt,QTimer,QFile,QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem, QSystemTrayIcon

from Ui_XeroxYor import *

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