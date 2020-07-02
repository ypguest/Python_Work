#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
生成mainlayout2 中所需要的界面， 包括Nick Name Query, Product ID Query, Function 按钮等布局
"""

import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# -------生成Product查询的ListView, 给出Nick Name-----------
class NickNameQuery(QWidget):
    sendmsg = pyqtSignal(str)

    def __init__(self):
        super(NickNameQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product Family Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = ProdList("Nick_Name")     # 创建数据源
        listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(listModel)             # 模型与空间关联
        self.listview.clicked.connect(self.clicked)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product Family")
        self.Button1 = QPushButton("OK")
        self.Button1.setFixedWidth(35)
        self.Button1.clicked.connect(self.sendEditContent)

        # todo 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.listview, 1, 0, 3, 4)
        layout.addWidget(self.lineEdit, 5, 0, 1, 3)
        layout.addWidget(self.Button1, 5, 3, 1, 1)

        self.groupbox.setLayout(layout)

    def clicked(self, qModelIndex):  # 点击后将值输入到LineEdit内
        self.lineEdit.setText(self.list[qModelIndex.row()])

    def sendEditContent(self):
        content = self.lineEdit.text()
        self.sendmsg.emit(content)


# -------生成Product_ID与Product_Version的联和查询listView, 给出Product_ID, Version---------
class ProdQuery(QWidget):
    def __init__(self):
        super(ProdQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product and Version Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 设置栅格布局

        self.listviewPid = QListView()
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listPid = ProdList("UniIC_Product_ID")     # 通过数据库查询Product_ID, 并根据结果创建数据源

        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联
        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中

        self.listviewVer = QListView()
        self.listModeVer = QStringListModel()           # 创建封装列表数据源的模型
        self.listVer = ProdList("UniIC_Product_Version")     # 创建数据源
        self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        self.listviewVer.setModel(self.listModeVer)             # 模型与空间关联
        self.listviewVer.clicked.connect(self.clickedVer)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product ID & Ver")

        # todo 设置所有控件布局
        layout.addWidget(self.listviewPid, 0, 0, 1, 1)  # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.listviewVer, 0, 1, 1, 1)               # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.lineEdit, 1, 0, 1, 2)

        self.groupbox.setLayout(layout)

    def clickedPid(self, qModelIndex):
        self.lineEdit.setText(self.listPid[qModelIndex.row()])      # 将LineEdit里的内容进行写入
        self.listviewVer = ProdQueryVerList(self.listPid[qModelIndex.row()])     # 创建数据源
        self.listModeVer.setStringList(self.listviewVer)  # 将数据和模型进行关联

    def clickedVer(self, qModelIndex):
        if self.lineEdit.text() is None:
            self.lineEdit.setText(self.listviewVer[qModelIndex.row()])
        elif len(self.lineEdit.text().split(",")) < 2:
            self.lineEdit.setText(self.lineEdit.text() + ',' + self.listviewVer[qModelIndex.row()])
        else:
            self.lineEdit.setText(self.lineEdit.text().split(",")[0] + ',' + self.listviewVer[qModelIndex.row()])

    def getmsg(self, val):
        self.listPid = ProdQueryIdList(val)
        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联
        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中


# -------根据输入的Text（Lot id, Comment），查询对应的Lot History
class TextQuery(QWidget):
    def __init__(self):
        super(TextQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Lot && Comment Query', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QVBoxLayout()                    # 设置栅格布局
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Please Input Lot ID or Commnet, split by ','")
        self.lotQueryButton = QPushButton("Lot Query")
        self.comQueryButton = QPushButton("Comment Query")
        self.clearButton = QPushButton("Clear All")

        layout.addWidget(self.textEdit)
        layout.addWidget(self.lotQueryButton)
        layout.addWidget(self.comQueryButton)
        layout.addWidget(self.clearButton)
        self.groupbox.setLayout(layout)


class FunButton(QWidget):
    def __init__(self):
        super(FunButton, self).__init__()
        self.setFixedSize(200, 200)

        self.groupbox = QGroupBox('WIP Query', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(200, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QVBoxLayout()

        self.WipButton = QPushButton("Daily WIP Check")
        self.LotButton = QPushButton("Product Lot Check")
        self.ShipButton = QPushButton("Product Shipping Check")
        self.QButton = QPushButton("Product Q-Time Check")
        self.spacerFunTop = QSpacerItem(1, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)  # 增加竖向弹簧线

        layout.addItem(self.spacerFunTop)
        layout.addWidget(self.WipButton)
        layout.addWidget(self.LotButton)
        layout.addWidget(self.ShipButton)
        layout.addWidget(self.QButton)

        self.groupbox.setLayout(layout)


# todo 用于class ProdQuery中, 用于给出关键字Item，并查找psmc_product_version表中所以的匹配值
def ProdList(item):
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
            cursor.execute('SELECT DISTINCT %s FROM psmc_product_version ORDER By %s' % (item, item))
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# todo 用于Class ProdQuery中, 用于给定UniIC_Product_Id，查找出对应的所有UniIC_Product_Version
def ProdQueryVerList(item):
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
            cursor.execute("SELECT DISTINCT UniIC_Product_Version FROM psmc_product_version WHERE UniIC_Product_Id = '%s' ORDER By UniIC_Product_Version" % item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# todo 用于Class ProdQuery中, 用于给定UniIC_Product_Id，查找出对应的所有UniIC_Product_Version
def ProdQueryIdList(item):
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
            cursor.execute("SELECT DISTINCT UniIC_Product_ID FROM psmc_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_ID" % item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = FunButton()
    main.show()
    sys.exit(app.exec_())
