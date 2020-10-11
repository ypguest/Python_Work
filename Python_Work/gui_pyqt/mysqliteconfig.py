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


def CheckDB():
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("./db/database.db")   # 如果数据库不存在，则会自动创建；如果存在，则采用该数据库
    if not database.open():
        QMessageBox.critical(None, "错误",
                             "无法建立到数据库的连接", QMessageBox.Cancel)
        return False
    else:
        query = QSqlQuery()
        select_sql = "select * from tempdb;"
        query.exec(select_sql)
        while query.next():
            print(query.value(1))
        return True


def closeDB(database):
    database.close()


def writeDB(data):
    con = sqlite3.connect("./db/database.db")
    pd.io.sql.to_sql(data, "tempdb", con=con,  if_exists='replace')

def func():
    model = QSqlTableModel()
    model.setTable("tempdb")
    model.setEditStrategy(QSqlTableModel.OnFieldChange)
    model.select()
    view = QTableView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    CheckDB()
    func()






