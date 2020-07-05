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
class FamilyQuery(QWidget):
    sendToProQuery = pyqtSignal(str)   # 发送至Product Query的信号
    sendmsg = pyqtSignal(str)   # 发送至MainLayout3的信号

    def __init__(self):
        super(FamilyQuery, self).__init__()
        self.setFixedSize(300, 200)

        # ------------设置框体--------------
        self.groupbox = QGroupBox('Product Family Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        # ------------设置布局---------------
        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        self.listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = ProdList("Nick_Name")     # 创建数据源
        self.listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(self.listModel)             # 模型与空间关联

        # ------------将listview的点击进行绑定----------
        self.listview.clicked.connect(self.clicked)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product Family")

        # todo 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.listview, 1, 0, 3, 4)
        layout.addWidget(self.lineEdit, 5, 0, 1, 4)

        self.groupbox.setLayout(layout)

    def clicked(self, qModelIndex):  # 点击后将值输入到LineEdit内
        self.lineEdit.setText(self.list[qModelIndex.row()])
        self.sendToProQuery.emit(self.list[qModelIndex.row()])

    def sendMsg(self):
        self.sendmsg.emit(self.lineEdit.text())


# -------生成Product_ID与Product_Version的联和查询listView, 给出Product_ID, Version---------
class ProdQuery(QWidget):
    sendmsg = pyqtSignal(str)    # 自定义信号

    def __init__(self):
        super(ProdQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product and Version Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 设置栅格布局

        # ----------------Product ID QListView设置---------------------
        self.listviewPid = QListView()
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listPid = ProdList("UniIC_Product_ID")     # 通过数据库查询Product_ID, 并根据结果创建数据源

        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联
        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中

        # ----------------Product Version QListView设置---------------------
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
        self.lineEdit.setText(self.listPid[qModelIndex.row()])      # 将LineEdit里的内容进行写入lineEdit
        self.listVer = ProdQueryVerList(self.listPid[qModelIndex.row()])     # 创建数据源
        self.listModeVer.setStringList(self.listVer)  # 将数据和模型进行关联
        self.listviewVer.setModel(self.listModeVer)  # 模型与空间关联

    # ---------定义单击List中的Ver事件，如果当lineEdit.text()为空时，则将版本放入;
    def clickedVer(self, qModelIndex):
        if self.lineEdit.text() == '':
            self.lineEdit.setText(self.listVer[qModelIndex.row()])
        elif len(self.lineEdit.text().split(",")) == 1:
            if self.lineEdit.text() in self.listVer:
                self.lineEdit.setText(self.listVer[qModelIndex.row()])
            else:
                self.lineEdit.setText(self.lineEdit.text() + ',' + self.listVer[qModelIndex.row()])
        elif len(self.lineEdit.text().split(",")) == 2:
            self.lineEdit.setText(self.lineEdit.text().split(",")[0] + ',' + self.listVer[qModelIndex.row()])
        else:
            pass

    def getMsg(self, value):
        self.lineEdit.setText('')
        self.listPid = InputQueryId(value)
        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联

        self.listVer = InputQueryVer(value)     # 创建数据源
        self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        self.listviewVer.setModel(self.listModeVer)             # 模型与空间关联

        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中

    def sendMsg(self):
        self.sendmsg.emit(self.lineEdit.text())


class FunButton(QWidget):
    sendmsg = pyqtSignal(str)

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

        # -------绑定函数-----------------------
        self.WipButton.clicked.connect(self.sendMsg)
        self.LotButton.clicked.connect(self.sendMsg)
        self.ShipButton.clicked.connect(self.sendMsg)
        self.QButton.clicked.connect(self.sendMsg)

        self.groupbox.setLayout(layout)

    def sendMsg(self):
        self.sendmsg.emit(self.sender().text())


# -------根据输入的Text（Lot id, Comment），查询对应的Lot History-----------------------
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


# -------用于class ProdQuery中, 输入Item(Product_ID or Ver)，并查找psmc_product_version表中所有的匹配值(List)-----------
def ProdList(Item):
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
            cursor.execute('SELECT DISTINCT %s FROM psmc_product_version ORDER By %s' % (Item, Item))
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# -------用于Class ProdQuery中, 输入UniIC_Product_Id（1G-H45），查找出对应的所有UniIC_Product_Version(V05)---
def ProdQueryVerList(Item):
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
            cursor.execute("SELECT DISTINCT UniIC_Product_Version FROM psmc_product_version WHERE UniIC_Product_Id = '%s' ORDER By UniIC_Product_Version" % Item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# ------用于Class ProdQuery中, 输入Nick_Name，查找出对应的所有UniIC_Product_ID
def InputQueryId(Item):
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
            cursor.execute("SELECT DISTINCT UniIC_Product_ID FROM psmc_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_ID" % Item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# ------用于Class ProdQuery中, 输入Nick_Name，查找出对应的所有UniIC_Product_Version
def InputQueryVer(Item):
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
            cursor.execute("SELECT DISTINCT UniIC_Product_Version FROM psmc_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_Version" % Item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main1 = FamilyQuery()
    main2 = ProdQuery()
    main3 = FunButton()
    main4 = TextQuery()
    main1.move(0, 0)
    main2.move(300, 300)
    main3.move(600, 600)
    main4.move(900, 900)
    main1.show()
    main2.show()
    main3.show()
    main4.show()
    sys.exit(app.exec_())