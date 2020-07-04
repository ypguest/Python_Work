#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
生成mainlayout3 中所需要的table界面， 包括根据Product Query的响应函数，已执行相应的查询动作
"""

import sys
import pandas as pd
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class WipTable(QWidget):
    def __init__(self):
        self.productFam = ''
        self.productId = ''
        self.productVer = ''

        super(WipTable, self).__init__()

        # ----------------定义布局，控件-------------
        layout = QHBoxLayout()

        # --------------定义QtableView控件----------
        self.TableWidget = QTableView()
        self.model = ''

        # --------设置Table的格式-----------------
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 表格禁止编辑
        self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)   # 按行选择
        self.TableWidget.setAlternatingRowColors(1)                  # 行间隔变色（boolen）

        layout.addWidget(self.TableWidget)
        self.setLayout(layout)

    def getQue1Msg(self, value):
        self.productFam = value

    def getQue2Msg(self, value):
        try:
            self.productId, self.productVer = value.split(',')
        except ValueError:
            self.productId = ''
            self.productVer = ''

    def getFunMsg(self, value):
        if value == 'Daily WIP Check':
            if self.productFam != '':
                if self.productId != '':
                    if self.productVer != '':
                        ProductId = ProductIdQuery1(self.productFam, self.productId, self.productVer)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
                    else:
                        ProductId = ProductIdQuery2(self.productFam, self.productId)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
                else:
                    if self.productVer != '':
                        ProductId = ProductIdQuery3(self.productFam, self.productVer)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
                    else:
                        ProductId = ProductIdQuery4(self.productFam)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
            else:
                if self.productId != '':
                    if self.productVer != '':
                        ProductId = ProductIdQuery5(self.productId, self.productVer)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
                    else:
                        ProductId = ProductIdQuery6(self.productId)
                        df = pd.DataFrame()
                        for i in ProductId:
                            df = df.append((ProductLotQuery(''.join(i))))
                        self.model = PandasModel(df)
                        self.TableWidget.setModel(self.model)
                else:
                    print('please input Product ID')

        # if value == 'Product Lot Check':
        #     pass
        # if value == 'Product Shipping Check':
        #     pass
        # if value == 'Product Q-Time Check':
        #     pass


class PandasModel(QAbstractTableModel):
    """定义了一个类，将dataframe写入并以table展现"""

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


# ---------------返回查询的数据--------------------
def ProductLotQuery(queryItem):

    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    sql = """
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%Y/%m/%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Comment, Fab, Layer, Stage, 
        DATE_FORMAT(`Current_Time`,'%Y/%m/%d %H:%i') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%Y/%m/%d') AS `Forecast_Date`, Qty, 
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` 
        FROM psmc_lot_tracing_table
        WHERE Current_Chip_Name = '{}'
        ORDER BY `Current_Time` DESC
        """ .format(queryItem)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取表头
    df = pd.DataFrame([pd.Series(i, index=columnNames).astype(str) for i in sql_results], columns=columnNames)  # 将从数据库中取出的元祖数据转换为dataframe
    for index, row in df.iterrows():    # 如果Qty 为0, 则将数据删除
        if row['Qty'] == '0':
            df.drop(index, inplace=True)
    return df


def ProductIdQuery1(productFam, productId, productVer):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE Nick_Name = '{}' AND UniIC_Product_ID = '{}' AND UniIC_Product_Version = '{}'
        """ .format(productFam, productId, productVer)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


def ProductIdQuery2(productFam, productId):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE Nick_Name = '{}' AND UniIC_Product_ID = '{}'
        """ .format(productFam, productId)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


def ProductIdQuery3(productFam, productVer):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE Nick_Name = '{}' AND UniIC_Product_Version = '{}'
        """ .format(productFam, productVer)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


def ProductIdQuery4(productFam):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE Nick_Name = '{}'
        """ .format(productFam)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


def ProductIdQuery5(productId, productVer):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE UniIC_Product_ID = '{}' AND UniIC_Product_Version = '{}'
        """ .format(productId, productVer)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


def ProductIdQuery6(productId):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    sql = """
        SELECT PowerChip_Product_ID FROM psmc_product_version WHERE UniIC_Product_ID = '{}'
        """ .format(productId)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE configdb;')
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        connection.close()
    sql_results = [list(i) for i in sql_results]
    return sql_results


if __name__ == '__main__':
    app = QApplication(sys.argv)
    product = 'AAPS70D1D-0E01'
    main = WipTable(product)
    main.show()
    sys.exit(app.exec_())


