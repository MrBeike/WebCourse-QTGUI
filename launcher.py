# -*- coding: utf-8 -*-

__author__ = 'xeroxYor'
import sys
import logging

from PyQt5.QtWidgets import QApplication

# resource import
import resource.webcourse_rc
# Window Defination import
from window.MainWindow import MainWindow


if __name__ == '__main__':
    logging.basicConfig(filename='DebugInfo',level=logging.DEBUG)
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())