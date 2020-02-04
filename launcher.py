# -*- coding: utf-8 -*-

__author__ = 'xeroxYor'

import os
import sys
import os.path

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path = [os.path.join(myFolder, 'ui'),
            os.path.join(myFolder, 'resource'),
            os.path.join(myFolder, 'api'),
            os.path.join(myFolder, 'window')
            ] + sys.path

os.chdir(myFolder)


from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

# TODO 实验室增加注册过期课程功能
# TODO 实验室增加下载课程视频功能
# TODO 消息收集器 每个按钮结束响应
# TODO 打包方式  文件夹释放模式？



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWinow = MainWindow()
    mainWinow.show()
    sys.exit(app.exec_())
