# -*- coding: utf-8 -*-

__author__ = 'xeroxYor'
import sys

from PyQt5.QtWidgets import QApplication

# resource import
import resource.webcourse_rc
# Window Defination import
from window.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())