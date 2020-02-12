# -*- coding: utf-8 -*-

__author__ = 'xeroxYor'
import sys

from PyQt5.QtWidgets import QApplication


import resource.webcourse_rc
# Window Defination import
from window.MainWindow import MainWindow


# TODO 实验室增加注册过期课程功能
# TODO 实验室增加下载课程视频功能
# TODO 打包方式  文件夹释放模式？



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())