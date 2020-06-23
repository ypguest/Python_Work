"""
生成Product查询的ListView, 给出Nick Name
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql


class ProdQuery1(QWidget):
    def __init__(self):
        super(ProdQuery, self).__init__()
        self.setFixedSize(300, 200)

        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = prodlist("Nick_Name")     # 创建数据源
        listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(listModel)             # 模型与空间关联
        self.listview.clicked.connect(self.clicked)
        layout.addWidget(self.listview, 0, 0, 4, 4)               # 将控件放入栅格布局，起始行，列，跨越行，列
        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.Button1 = QPushButton("OK")
        self.Button1.setFixedWidth(35)
        layout.addWidget(self.lineEdit, 5, 0, 1, 3)
        layout.addWidget(self.Button1, 5, 3, 1, 1)

        self.setLayout(layout)

    def clicked(self, qModelIndex):
        self.lineEdit.setText(self.list[qModelIndex.row()])


class ProdQuery2(QWidget):
    def __init__(self):
        super(ProdQuery2, self).__init__()
        self.setFixedSize(300, 200)

        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = prodlist("UniIC_Product_ID")     # 创建数据源
        listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(listModel)             # 模型与空间关联
        self.listview.clicked.connect(self.clicked)
        layout.addWidget(self.listview, 0, 0, 4, 4)               # 将控件放入栅格布局，起始行，列，跨越行，列
        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.Button1 = QPushButton("OK")
        self.Button1.setFixedWidth(35)
        layout.addWidget(self.lineEdit, 5, 0, 1, 3)
        layout.addWidget(self.Button1, 5, 3, 1, 1)

        self.setLayout(layout)

    def clicked(self, qModelIndex):
        self.lineEdit.setText(self.list[qModelIndex.row()])


def prodlist(item):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE configdb;')
            cursor.execute('SELECT distinct %s FROM psmc_product_version' % item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ProdQuery()
    main.show()
    sys.exit(app.exec_())
