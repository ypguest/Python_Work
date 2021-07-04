# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel


class DataGrid(QWidget):

    """
    1. 通过DG访问TEMP数据库，对TEMP数据库进行编辑，并将修改内容返回MYSQL数据库（X）
    2. 筛选功能实现，按条件？？？(X)
    3. 排序功能，界面实现(X)
    4. 画当前WIP图(X)
    5. 增加上浮信息，能够显示这个lot的Wafer信息(X)
    6. 增加点击右键增加/减少行功能(X)
    7. 按列禁止修改(X)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("获取Temp数据")

        # ---- 声明相关变量 ----
        self.db = QSqlDatabase.addDatabase("QSQLITE")

        self.tableData = None

        # ---- 查询模型 ----
        self.queryModel = QSqlTableModel(db=self.db)

        self.queryModel.setEditStrategy(QSqlTableModel.OnFieldChange)    # 所有变更实时更新到数据库中
        self.proxyModel = QSortFilterProxyModel()     # 通过代理模型增加排序功能
        self.proxyModel.setFilterKeyColumn(0)
        self.proxyModel.setSourceModel(self.queryModel)   # 将筛选模型赋给Sqltable模型


        # ---- 设置表格属性 ----
        self.tableView = QTableView()

        # ---- 设置tableView选项 ----
        self.tableView.setModel(self.proxyModel)    # 将模型绑定

        self.tableView.verticalHeader().setVisible(False)    # 隐藏行名称
        self.tableView.setSortingEnabled(True)    # 排序功能
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)   # 表示均匀拉直表头
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        # self.tableView.setItemDelegateForColumn(2, EmptyDelegate(self))

        # ---- 将tableView部署 ----
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.tableView)
        self.setLayout(mainLayout)

        # ---- 设置连接 ----
        self.queryModel.beforeUpdate.connect(self.changeItem)
        # self.tableView.clicked_rightMenu()
        # self.switchPageButton.clicked.connect(self.onSwitchPage)

    def changeItem(self):
        index = self.tableView.selectedIndexes()
        for i in index():
            print(i)


    def setTableView(self):

        self.db.setDatabaseName("./db/database.db")  # 如果数据库不存在，则会自动创建；如果存在，则采用该数据库
        self.db.open()
        self.queryModel.setTable('tempdb')
        self.queryModel.select()
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(2)
        self.tableView.hideColumn(8)

    def writeData(self, data):
        """向数据库中写入内容"""
        con = sqlite3.connect("./db/database.db")
        pd.io.sql.to_sql(data, "tempdb", con=con, if_exists='replace')
        self.tableData = data


# class TableViewModel(QSqlTableModel):
#
#     def __init__(self):
#         super(TableViewModel, self).__init__()
#
#     def flags(self, modelIndex):
#         if not modelIndex.isValid():
#             return
#         if modelIndex.column() != 1 and modelIndex.column() != 4:
#             return Qt.ItemIsEnabled | Qt.ItemIsSelectable
#         return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
#
#     def data(self, modelIndex, role=Qt.DisplayRole):
#         if not modelIndex.isValid():
#             return QVariant()
#
#         if role != Qt.DisplayRole & role != Qt.EditRole:
#             return QVariant()
#
#         return record.value(modelIndex.column())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataGrid()
    main.setTableView()
    index = main.queryModel.index(0, 3, QModelIndex())
    index1 = index.siblingAtColumn(6)
    main.show()
    sys.exit(app.exec_())






