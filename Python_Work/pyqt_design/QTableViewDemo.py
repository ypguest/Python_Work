"""
显示二维表数据（QTableView控件）

数据源（Model）
需要创建QTableView实例和一个数据源（Model）,然后将两者关联；
MVC: Model Viewer Controller
使用MVC的方式，可以将后端的数据与前段页面的耦合度降低
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TableViewDemo(QWidget):
    def __init__(self):
        super(TableViewDemo, self).__init__()
        self.setWindowTitle('QtableView表格视图控件演示')

        # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setGeometry(100, 100, self.width-200, self.height-200)   # setGeometry(x_noFrame, y_noFrame, width, height)与resize(width, height)作用相同, 但是参数不同

        # 准备数据模型
        self.model = QStandardItemModel(4, 3)
        self.model.setHorizontalHeaderLabels(['id', '姓名', '年龄'])

        self.tableview = QTableView()
        # 关联QtableView控件和Model
        self.tableview.setModel(self.model)

        # 添加数据
        item11 = QStandardItem('10')
        item12 = QStandardItem('雷神')
        item13 = QStandardItem('2000')
        self.model.setItem(0, 0, item11)
        self.model.setItem(0, 1, item12)
        self.model.setItem(0, 2, item13)

        layout = QVBoxLayout()
        layout.addWidget(self.tableview)
        self.setLayout(layout)

        # 添加数据
        item11 = QStandardItem()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TableViewDemo()
    main.show()
    sys.exit(app.exec_())

