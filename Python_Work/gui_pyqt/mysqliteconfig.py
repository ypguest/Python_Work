# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:mysqliteconfig.py
# @Time:2020/10/11 11:36
# @Author:Jason_Yin

import sys
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel


class DataGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分页查询例子")

        # ---- 声明数据库连接 ----
        self.db = QSqlDatabase.addDatabase("QSQLITE")

        # ---- 查询模型 ----
        self.queryModel = QSqlTableModel()
        self.queryModel.setEditStrategy(QSqlTableModel.OnFieldChange)    # 所有变更实施更新中数据库中

        # ---- 设置表格属性 ----
        self.tableView = QTableView()
        self.tableView.verticalHeader().setVisible(False)

        self.tableView.setModel(self.queryModel)

        # ---- 按钮定义 ----
        self.prevButton = QPushButton("Prev")
        self.nextButton = QPushButton("Next")
        self.switchPageButton = QPushButton("Switch")

        # ---- 总页数文本 ----
        self.totalPageLabel = QLabel()
        # ---- 当前页文本 ----
        self.currentPageLabel = QLabel()
        # ---- 转到页输入框 ----
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)
        # ---- 当前页 ----
        self.currentPage = 0
        # ---- 总页数 ----
        self.totalPage = 0
        # ---- 总记录数 ----
        self.totalRecordCount = 0
        # ---- 每页记录数 ----
        self.pageRecordCount = 10

        # ---- 操作布局 ----
        self.tableView.horizontalHeader().setStretchLastSection(True)  # 将最后一列填充满表格
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # 表示均匀拉直表头

        operatorLayout = QHBoxLayout()

        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        operatorLayout.addWidget(QLabel("转到第"))
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(QLabel("页"))
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addWidget(QLabel("当前页："))
        operatorLayout.addWidget(self.currentPageLabel)
        operatorLayout.addWidget(QLabel("总页数："))
        operatorLayout.addWidget(self.totalPageLabel)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.tableView)
        mainLayout.addLayout(operatorLayout)
        self.setLayout(mainLayout)

        # # ---- 设置连接 ----
        # self.prevButton.clicked.connect(self.onPrevPage)
        # self.nextButton.clicked.connect(self.onNextPage)
        # self.switchPageButton.clicked.connect(self.onSwitchPage)

    def setTableView(self):
        self.db.setDatabaseName("./db/database.db")  # 如果数据库不存在，则会自动创建；如果存在，则采用该数据库
        if not self.db.open():
            return False
        self.queryModel.setTable('tempdb')
        self.queryModel.select()
        self.queryModel.setFilter("1=1 limit 1,1;")
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(2)

    @staticmethod
    def wirteData(data):
        """向数据库中写入内容"""
        con = sqlite3.connect("./db/database.db")
        pd.io.sql.to_sql(data, "tempdb", con=con, if_exists='replace')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataGrid()
    main.setTableView()
    main.show()
    sys.exit(app.exec_())






