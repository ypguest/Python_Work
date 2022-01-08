# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from PyQt5.sip import *
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_MainWindow import Ui_MainWindow
from my_Function import (prodIdCov, getProductId, DailyWipCheck, ProdFamList, ProdList, ProdQueryVerList, InputQueryId, InputQueryVer,
                         HistoryQuery_psmc, HistoryQuery_xmc)
from my_SqlConfig import MySQLite
from my_DataGrid import QTabDataGrid, QMapDataGridWip, QMapDataGridHis

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.MainWindow = Ui_MainWindow()
        self.MainWindow.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(r'../GuiScrip/images/ico/UniIC_Logo.ico'))

        # =================== 参数定义 =======================
        self.fab = 'PSMC'
        self.prodFam = ''
        self.proName = '' 
        self.proVer = ''
        self.func_button = ''

        # ================== 数据录入 =======================
        # ========== Product Family QListView设置 ==========
        self.listModelFam = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewFam = ProdFamList("Nick_Name")     # 创建数据源, 查询Product_Version中Nick_Name的列表
        self.listModelFam.setStringList(self.listViewFam)       # 将数据和模型进行关联
        self.MainWindow.box1View.setModel(self.listModelFam)             # 模型与空间关联

        # ========== Product ID QListView设置 ===========
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewPid = ProdList("UniIC_Product_ID", self.fab)  # 通过数据库查询Product_ID, 并根据结果创建数据源
        self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
        self.MainWindow.box2prodList.setModel(self.listModelPid)             # 模型与控件关联

        # 属性设置
        self.MainWindow.box2prodList.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.MainWindow.box2prodList.clicked.connect(self.clickedPid)

        # ========== Product Version QListView设置 ==========
        self.listModeVer = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源
        self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联
        self.MainWindow.box2VerList.setModel(self.listModeVer)             # 模型与空间关联

        # 属性设置
        self.MainWindow.box2VerList.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.MainWindow.box2VerList.clicked.connect(self.clickedVer)

    # ========== 由connectSlotsByName() 自动连接的槽函数==================
    def on_box1View_clicked(self, selectedIndexe):
        """ 若box1View内容被选中则将box1View选择的结果反馈到box1LineEdit中 """
        self.MainWindow.box1LineEdit.setText(self.listViewFam[selectedIndexe.row()])

    def on_box1LineEdit_textChanged(self):
        """ 若box1LineEdit的内容发生改变，则将该内容传递给 @self.prodFam """
        self.prodFam = self.MainWindow.box1LineEdit.text()
        # 根据@self.prodFam的内容更新self.listViewPid，self.listViewVer

        if len(self.prodFam) == 0:
            # ==== 如果ProdFam的数据为空，则根据Fab进行查询， 并更新@self.listViewPid，self.listViewVer ====
            self.listViewPid = ProdList("UniIC_Product_ID", self.fab)     # 通过数据库查询Product_ID, 并根据结果创建数据源
            self.listModelPid.setStringList(self.listViewPid)       # 将模型中的数据进行更新
            self.listViewVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将模型中的数据进行更新
        else:
            # ==== 如果ProdFam有数据，则根据ProdFam和Fab信息进行查询，并更新@self.listViewPid，self.listViewVer ====
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联
        # 将box2LineEdit重置
        self.MainWindow.box2LineEdit.setText("")

    def on_box2Button1_toggled(self, bools):
        """ 若box2Button1被选中，则将PSMC赋值给self.fab"""
        if bools:
            self.fab = 'PSMC'
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联

    def on_box2Button2_toggled(self, bools):
        """ 若box2Button1被选中，则将XMC赋值给self.fab"""
        if bools:
            self.fab = 'XMC'
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联

    def on_box3fcnbtn1_pressed(self):
        """当box3fcnbtn1被按下，则将相应的数据写入sqlite数据库"""
        productinfo = dict()
        self.func_button = 'Daily Wip'
        productinfo['Nick_Name'] = [self.prodFam]
        productinfo['Fab'] = [self.fab]
        productinfo['UniIC_Product_ID'], productinfo['UniIC_Product_Version'] = prodIdCov(self.MainWindow.box2LineEdit.text())
        columns = list(productinfo.keys())  # 获取参数名['Nick_Name','Fab','UniIC_Product_ID','UniIC_Product_Version']

        for key in columns:  # 如果参数为空，则去掉该参数
            if productinfo[key] == ['']:
                del productinfo[key]
        productid = getProductId(productinfo)  # 输入产品信息，生成PowerChip_Product_Version List字典
        curwip = DailyWipCheck(productid, productinfo['Fab'])

        # 将数据写至SQLite数据库
        mysql = MySQLite()
        mysql.update_df(curwip)
        self.creatTab(self.MainWindow.tabWidget.currentIndex())        # 基于SQlite上的数据展示到tabwiget上

    def on_box4fcnbtn1_pressed(self):
        self.func_button = 'Lot History Query'
        text_infor = self.MainWindow.box4textEdit.toPlainText()   # 获取需要进行查询的lot ID
        # ==== 将输入的信息转换为以6位字符为单元的list ====
        if len(text_infor) == 0:
            lot_infor = ['']
        else:
            try:
                lot_infor = re.split(r'[,，]', text_infor)
            except:
                lot_infor = text_infor.copy()

        lot_infor = [x.strip(' ') for x in lot_infor]
        for i in range(len(lot_infor)):
            if len(lot_infor[i]) < 6:
                del lot_infor[i]
            else:
                lot_infor[i] = lot_infor[i][:6]
        curwip1 = HistoryQuery_psmc(lot_infor)
        curwip2 = HistoryQuery_xmc(lot_infor)
        curwip = curwip1.append(curwip2)

        # 将数据写至SQLite数据库
        mysql = MySQLite()
        mysql.update_df(curwip)

        # 基于SQlite上的数据展示到tabwiget上
        self.creatTab(self.MainWindow.tabWidget.currentIndex())

    def on_tabWidget_tabBarClicked(self, index):
        """当QtabWidget选项发生变化则进行更新"""
        self.creatTab(index)

    # ========== 由自定义函数连接的槽函数==================

    def clickedPid(self):
        """当数据进行切换时，将选中的Product ID数据放入LineEdit中"""
        datalist = list()
        for i in self.MainWindow.box2prodList.selectedIndexes():
            datalist.append(i.data())
        self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist) + ']')      # 将LineEdit里的内容进行写入lineEdit
        self.listViewVer = ProdQueryVerList(datalist    , self.fab)     # 创建数据源
        self.listModeVer.setStringList(self.listViewVer)  # 将数据和模型进行关联

    def clickedVer(self):
        """定义单击List中的Ver事件，如果当lineEdit.text()为空时，则将版本放入"""
        datalist = list()
        # ---- 将点击的内容变成list ----
        for i in self.MainWindow.box2VerList.selectedIndexes():
            datalist.append(i.data())
        if self.MainWindow.box2LineEdit.text() == '' or re.findall(r'\[V\d*\]', self.MainWindow.box2LineEdit.text()):
            self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist) + ']')  # 将LineEdit里的内容进行写入lineEdit
        else:
            matchobj = re.split(r'\[|\],\[|\]', self.MainWindow.box2LineEdit.text())
            matchobj = [i for i in matchobj if i != '']
            for i in range(len(matchobj)):
                if matchobj[i].split(','):
                    matchobj[i] = matchobj[i].split(',')[0]
            datalist1 = []
            for i in range(len(matchobj)):
                for j in range(len(datalist)):
                    datalist1.append(matchobj[i] + ',' + datalist[j])
            self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist1) + ']')

    def creatTab(self, index):
        """若tabWiget在列表界面，则显示数据列表"""
        # =========== 显示Daily wip的列表 =================
        if index == 0 and self.func_button == 'Daily Wip':
            delete(self.MainWindow.tabWidget.widget(0))
            myDataGrid = QTabDataGrid()
            self.MainWindow.tabWidget.insertTab(0, myDataGrid, 'Tab 1')
            self.MainWindow.tabWidget.setCurrentIndex(0)
        # =========== 显示Daily wip的图 ==================
        if index == 1 and self.func_button == 'Daily Wip':
            delete(self.MainWindow.tabWidget.widget(1))
            myDataGrid = QMapDataGridWip(fab=self.fab, db='tempdb')
            self.MainWindow.tabWidget.insertTab(1, myDataGrid, 'Tab 2')
            self.MainWindow.tabWidget.setCurrentIndex(1)
        # =========== 显示DLot History 的列表 =============
        if index == 0 and self.func_button == 'Lot History Query':
            delete(self.MainWindow.tabWidget.widget(0))
            myDataGrid = QTabDataGrid()
            self.MainWindow.tabWidget.insertTab(0, myDataGrid, 'Tab 1')
            self.MainWindow.tabWidget.setCurrentIndex(0)
        # =========== 显示DLot History 的图 =============
        if index == 1 and self.func_button == 'Lot History Query':
            delete(self.MainWindow.tabWidget.widget(1))
            myDataGrid = QMapDataGridHis(db='tempdb')
            self.MainWindow.tabWidget.insertTab(1, myDataGrid, 'Tab 2')
            self.MainWindow.tabWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindows()
    main.show()
    sys.exit(app.exec_())
