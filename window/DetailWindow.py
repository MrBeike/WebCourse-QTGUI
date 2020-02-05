# -*- coding: utf-8 -*-
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot,Qt,QTimer,QFile,QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow,QHeaderView,QMessageBox,QDialog,QTableWidgetItem, QSystemTrayIcon

from Ui_DetailWindow import *

from Learn import Learn

# 项目内课程详细信息窗体
class DetailWindow(QDialog,Ui_DetailWindow):
    def __init__(self,projectName,projectId,parent=None):
        super(DetailWindow, self).__init__(parent)
        self.setupUi(self)
        self.project_name_label.setText(str(projectName))
        self.project_id_label.setText(str(projectId))
        qss_file = QFile(":/QSS/style.qss")
        qss_file.open(QFile.ReadOnly)
        qss_content= QTextStream(qss_file)
        self.qss = qss_content.readAll()
        self.setStyleSheet(self.qss)

    '''
    Table Model Defination
    '''
    def project_detail_list_initial(self,project_detail_result):
        # 建立数据模型实例
        self.project_detail_list_model = QStandardItemModel()
        # 设置列标题
        header = ['课程名称', '学时','测试得分','是否完成','课程编号']
        self.project_detail_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if project_detail_result:
            row, col = len(project_detail_result), len(project_detail_result[0])
            for row, datadict in enumerate(project_detail_result):
                datalist = [datadict['name'],datadict['time'],datadict['score'],datadict['finished'],datadict['id']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.project_detail_list_model.setItem(row, col, value)
            # 添加模型到QTableView实例中
            self.project_detail_list.setModel(self.project_detail_list_model)
        
            self.project_detail_list.setColumnWidth(0,440)
            self.project_detail_list.setColumnWidth(1,40)
            self.project_detail_list.setColumnWidth(2,70)
            self.project_detail_list.setColumnWidth(3,70)
            self.project_detail_list.setColumnWidth(4,0)
            self.project_detail_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    '''
    Slot Defination
    '''
    @pyqtSlot()
    def on_learn_button_clicked(self):
        row = self.project_detail_list.currentIndex().row()
        courseId = self.project_detail_list_model.index(row, 4).data()
        courseTime = self.course_list_model.index(row,1).data()
        # 为了函数的一致性，此处构建包含一个信息点的list [{,,,}]
        courseLists = [{
            'id':courseId,
            'time':courseTime
        }]
        learn = Learn(self.s)
        notify = learn.learn(courseLists)
        notify_result = notify.show()
        self.notifywindow = NotifyWindow()
        self.notifywindow.notify_list_initial(notify_result)
        self.notifywindow.show()
        self.project_detail_list_model.clear()
        project_detail_result = Learn.projectDetailReader(projectId)
        self.project_detail_list_initial(project_detail_result)