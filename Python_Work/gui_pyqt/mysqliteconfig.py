# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:mysqliteconfig.py
# @Time:2020/10/11 11:36
# @Author:Jason_Yin

import sys
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


class DataGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("分页查询例子")

        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 总页数文本
        self.tatalPageLabel = None
        # 当前页文本
        self.currentPageLineEdit = None
        # 转到页输入框
        self.swithPageLabel = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.taotalRecordCount = 0

        # 操作布局
        operaorLayout = QHBoxLayout()






    def __init__(self, data):
        """向数据库中写入内容"""
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName(r"./db/database.db")   # 如果数据库不存在，则会自动创建；如果存在，则采用该数据库
        con = sqlite3.connect(r"./db/database.db")
        pd.io.sql.to_sql(data, "tempdb", con=con, if_exists='replace')
        # 创建并设置QSqlTableModel
        self.model = QSqlTableModel()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = [1]
    table = TempTable(data)






