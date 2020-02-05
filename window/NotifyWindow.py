# -*- coding: utf-8 -*-
class NotifyWindow(QDialog,Ui_NotifyWindow):
    def __init__(self,parent=None):
        super(NotifyWindow, self).__init__(parent)
        self.setupUi(self)
        qss_file = QFile(":/QSS/style.qss")
        qss_file.open(QFile.ReadOnly)
        qss_content= QTextStream(qss_file)
        self.qss = qss_content.readAll()
        self.setStyleSheet(self.qss)

    '''
    Table Model Defination
    '''
    def notify_list_initial(self,notify_result):
        # 建立数据模型实例
        self.notify_list_model = QStandardItemModel()
        # 设置列标题
        header = ['类型', '内容']
        self.notify_list_model.setHorizontalHeaderLabels(header)
        # 向模型添加数据
        if notify_result:
            row, col = len(notify_result), len(notify_result[0])
            for row, datadict in enumerate(notify_result):
                datalist = [datadict['type'],datadict['message']]
                for col, cell in enumerate(datalist):
                    value = QStandardItem(str(cell))
                    # 设置单元不可编辑
                    value.setEditable(False)
                    self.notify_list_model.setItem(row, col, value)
            # 添加模型到QTableView实例中
            self.notify_list.setModel(self.notify_list_model)
        
            self.notify_list.setColumnWidth(0,40)
            self.notify_list.setColumnWidth(1,580)
            self.notify_list.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    '''
    Slot Defination
    '''   