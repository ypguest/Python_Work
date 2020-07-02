#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
生成mainlayout3 中所需要的table界面， 包括根据Product Query的响应函数，已执行相应的查询动作
"""

import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import datetime
import pandas as pd
import numpy as np
import pymysql
import xlrd
from sqlalchemy import create_engine

class WipTable(QWidget):
    def __init__(self):
        super(WipTable, self).__init__()

        self.desktop = QApplication.desktop()
        self.resize(700, 500)

        layout = QHBoxLayout()

        product = 'AAPS70D1D-0E01'
        data = ProductLotQuery(product)
        DataRowCount = data.shape[0]       # 行
        DataColumnCount = data.shape[1]    # 列

        self.TableWidget = QTableWidget()
        self.TableWidget.setRowCount(DataRowCount)
        self.TableWidget.setColumnCount(DataColumnCount)
        self.TableWidget.setHorizontalHeaderLabels(list(data))

        # 添加数据
        # item11 = QStandardItem('10')
        # item12 = QStandardItem('雷神')
        # item13 = QStandardItem('2000')
        # self.model.setItem(0, 0, item11)
        # self.model.setItem(0, 1, item12)
        # self.model.setItem(0, 2, item13)

        layout.addWidget(self.TableWidget)
        self.setLayout(layout)

        # 添加数据
        item11 = QStandardItem()


# ---------------返回查询的数据--------------------
def ProductLotQuery(Item):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    sql = """
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%Y/%m/%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Current_Chip_Name, Fab, Layer, Stage, 
        DATE_FORMAT(`Current_Time`,'%Y/%m/%d %H:%i') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%Y/%m/%d') AS `Forecast_Date`, Qty, 
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` 
        FROM psmc_lot_tracing_table
        WHERE Current_Chip_Name = '{}'""" .format(Item)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取表头
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)  # 将从数据库中取出的元祖数据转换为dataframe
    df.drop_duplicates(subset=['Lot_ID'], keep='first', inplace=True)  # 将dataframe中Lot_id相同的数据，只保留第一次的
    return df


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = WipTable()
    main.show()
    sys.exit(app.exec_())


