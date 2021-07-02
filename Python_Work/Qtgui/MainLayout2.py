#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
生成mainlayout2 中所需要的界面， 包括Nick Name Query, Product ID Query, Function 按钮等布局
"""

import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mysqlconfig import MySQL


class FamilyQuery(QWidget):
    """ 查询窗体1，生成Product查询的ListView, 给出Nick Name """

    sendToProQuery = pyqtSignal(str)   # 将str信息发送至Product Query的信号
    sendToMain = pyqtSignal(str)   # 将str信息发送至MainLayout3的信号

    def __init__(self):
        super(FamilyQuery, self).__init__()
        self.setFixedSize(200, 200)

        # ---- 设置框体 ----
        self.groupbox = QGroupBox('Product Family Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(200, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        # ---- 设置布局 ----
        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        self.listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = ProdFamList("Nick_Name")     # 创建数据源, 查询Product_Version中Nick_Name的列表
        self.listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(self.listModel)             # 模型与空间关联

        # ---- 将listview的点击进行绑定 ----
        self.listview.clicked.connect(self.clicked)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product Family")
        self.lineEdit.setFont(QFont("等线", 8))

        # ---- 将lineEdit的变化进行绑定 ----
        self.lineEdit.textChanged.connect(self.changed)

        # ---- 将控件放入栅格布局，起始行，列，跨越行，列 ----
        layout.addWidget(self.listview, 1, 0, 3, 4)
        layout.addWidget(self.lineEdit, 5, 0, 1, 4)

        self.groupbox.setLayout(layout)

    def clicked(self, qModelIndex):
        """ 点击后将值输入到LineEdit内 """
        self.lineEdit.setText(self.list[qModelIndex.row()])

    def changed(self):
        """当LineEdit发生变化时，将str信息发送至Product Query组件"""
        self.sendToProQuery.emit(self.lineEdit.text())

    def sendMsg(self):
        """ 将str信息通过MainWidget发送至ProdQuery.getMsg"""
        self.sendToMain.emit(self.lineEdit.text())


class ProdQuery(QWidget):
    """ 生成Product_ID与Product_Version的联和查询listView, 给出Product_ID, Version """
    sendToMainL3 = pyqtSignal(str, str)    # 自定义信号

    def __init__(self):
        super(ProdQuery, self).__init__()
        self.fab = 'PSMC'
        self.ProdFam = None
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product and Version Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 设置栅格布局

        # ---- 对Fab信息进行选择 ----
        self.btnfab1 = QRadioButton('PSMC')
        self.btnfab2 = QRadioButton('XMC')
        self.btnfab1.setChecked(True)
        self.btnfab1.clicked.connect(self.clickedfab)
        self.btnfab2.clicked.connect(self.clickedfab)

        # ---- Product ID QListView设置 ----
        self.listviewPid = QListView()
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listPid = ProdList("UniIC_Product_ID", self.fab)     # 通过数据库查询Product_ID, 并根据结果创建数据源

        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联
        self.listviewPid.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中

        # ---- Product Version QListView设置 ----
        self.listviewVer = QListView()
        self.listModeVer = QStringListModel()           # 创建封装列表数据源的模型
        self.listVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源

        self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        self.listviewVer.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.listviewVer.setModel(self.listModeVer)             # 模型与空间关联
        self.listviewVer.clicked.connect(self.clickedVer)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product ID & Ver")
        self.lineEdit.setFont(QFont("等线", 8))

        # ---- ProdQuery中的控件布局 ----
        layout.addWidget(self.btnfab1, 0, 0, 1, 1)
        layout.addWidget(self.btnfab2, 0, 1, 1, 1)
        layout.addWidget(self.listviewPid, 1, 0, 1, 1)  # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.listviewVer, 1, 1, 1, 1)               # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.lineEdit, 2, 0, 1, 2)

        self.groupbox.setLayout(layout)

    # ---- 定义功能 ----
    def clickedfab(self):
        self.fab = self.sender().text()
        self.getMsg(self.ProdFam)   # 当更换了Fab，则需要更新产品列表框

    def clickedPid(self):
        """当数据进行切换时，将选中的Product ID数据放入LineEdit中"""
        datalist = list()
        for i in self.listviewPid.selectedIndexes():
            datalist.append(i.data())
        self.lineEdit.setText('[' + '],['.join(datalist) + ']')      # 将LineEdit里的内容进行写入lineEdit
        self.listVer = ProdQueryVerList(datalist, self.fab)     # 创建数据源
        self.listModeVer.setStringList(self.listVer)  # 将数据和模型进行关联

    def clickedVer(self):
        """定义单击List中的Ver事件，如果当lineEdit.text()为空时，则将版本放入"""
        datalist = list()
        # ---- 将点击的内容变成list ----
        for i in self.listviewVer.selectedIndexes():
            datalist.append(i.data())
        if self.lineEdit.text() == '' or re.findall(r'\[V\d*\]', self.lineEdit.text()):
            self.lineEdit.setText('[' + '],['.join(datalist) + ']')  # 将LineEdit里的内容进行写入lineEdit
        else:
            matchobj = re.split(r'\[|\],\[|\]', self.lineEdit.text())
            matchobj = [i for i in matchobj if i != '']
            for i in range(len(matchobj)):
                if matchobj[i].split(','):
                    matchobj[i] = matchobj[i].split(',')[0]
            datalist1 = []
            for i in range(len(matchobj)):
                for j in range(len(datalist)):
                    datalist1.append(matchobj[i] + ',' + datalist[j])
            self.lineEdit.setText('[' + '],['.join(datalist1) + ']')

    def getMsg(self, value):
        """通过MainWidget获取ProdQuery1的sendToMain中的数据，并更新相应的listPid，listVer"""
        self.ProdFam = value
        if value is None:
            # ---- 如果ProdFam的数据为空，则根据Fab进行查询 ----
            self.listPid = ProdList("UniIC_Product_ID", self.fab)     # 通过数据库查询Product_ID, 并根据结果创建数据源
            self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
            self.listVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        elif len(value) == 0:
            # ---- 如果ProdFam的数据为空，则根据Fab进行查询 ----
            self.listPid = ProdList("UniIC_Product_ID", self.fab)  # 通过数据库查询Product_ID, 并根据结果创建数据源
            self.listModelPid.setStringList(self.listPid)  # 将数据和模型进行关联
            self.listVer = ProdList("UniIC_Product_Version", self.fab)  # 创建数据源
            self.listModeVer.setStringList(self.listVer)  # 将数据和模型进行关联
        else:
            # ---- 如果ProdFam有数据，则根据ProdFam和Fab信息进行查询 ----
            self.listPid = InputQueryId(value, self.fab)
            self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联

            self.listVer = InputQueryVer(value, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        self.lineEdit.setText("")

    def sendMsg(self):
        """将Fab, 输入的产品信息进行发送"""
        self.sendToMainL3.emit(self.fab, self.lineEdit.text())


class FunButton(QWidget):
    """ 生成wip功能键 """
    sendToMainL3 = pyqtSignal(str)

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

        # ---- 绑定函数 ----
        self.WipButton.clicked.connect(self.sendMsg)
        self.LotButton.clicked.connect(self.sendMsg)
        self.ShipButton.clicked.connect(self.sendMsg)
        self.QButton.clicked.connect(self.sendMsg)

        self.groupbox.setLayout(layout)

    def sendMsg(self):
        self.sendToMainL3.emit(self.sender().text())


class TextQuery(QWidget):
    """根据输入的Text（Lot id, Comment），查询对应的Lot History"""

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


def ProdFamList(query1):
    """用于FamilyQuery & ProdQuery中, 输入Item(Product_ID or Ver)，并查找psmc_product_version表中所有的匹配值(List)"""
    # ---- 查询pmsc的nick_name
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM psmc_product_version ORDER By '%s'" % (query1, query1)
    desc1, result1 = mysql.sqlAll(sql)
    res1 = [result1[i][0] for i in range(len(result1))]

    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM xmc_product_version ORDER By '%s'" % (query1, query1)
    desc2, result2 = mysql.sqlAll(sql)
    res2 = [result2[i][0] for i in range(len(result2))]
    result = res1 + res2
    result = sorted(list(set(result))[:])
    return result


def ProdList(query1, fab):
    """用于FamilyQuery & ProdQuery中, 输入Item(Product_ID or Ver)，并查找psmc_product_version表中所有的匹配值(List)"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM %s_product_version ORDER By '%s'" % (query1, fab, query1)
    desc, result = mysql.sqlAll(sql)
    return sorted([result[i][0] for i in range(len(result))])


def ProdQueryVerList(items, fab):
    """用于ProdQuery中, 实现输入UniIC_Product_Id（1G-H45），查找出对应的所有UniIC_Product_Version(V05)"""
    results = list()
    mysql = MySQL()
    mysql.selectDb('configdb')
    for item in items:
        sql = "SELECT DISTINCT UniIC_Product_Version FROM %s_product_version WHERE UniIC_Product_Id = '%s' ORDER By UniIC_Product_Version" % (fab, item)
        desc, result = mysql.sqlAll(sql)
        results.extend([result[i][0] for i in range(len(result))])
    results = list(set(results))[:]
    for i in range(len(results)-1):
        if int(results[i+1].replace('V', '')) < int(results[i].replace('V', '')):
            for j in range(i+1, 0, -1):
                if int(results[j].replace('V', '')) < int(results[j-1].replace('V', '')):
                    results[j-1], results[j] = results[j], results[j-1]
                else:
                    break
    return sorted(results)


def InputQueryId(query, fab):
    """用于ProdQuery中, 实现输入Nick_Name，查找出对应的所有UniIC_Product_ID"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT UniIC_Product_ID FROM %s_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_ID" % (fab, query)
    desc, result = mysql.sqlAll(sql)
    return [result[i][0] for i in range(len(result))]


def InputQueryVer(query, fab):
    """用于ProdQuery中, 输入Nick_Name，查找出对应的所有UniIC_Product_Version"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT UniIC_Product_Version FROM %s_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_Version" % (fab, query)
    desc, result = mysql.sqlAll(sql)
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