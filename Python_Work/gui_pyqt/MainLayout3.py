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
from Python_Work.gui_pyqt.mysqlconfig import MySQL

pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


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

    def iniLocal(self):
        """将MainLayout3中的查询讯息初始化"""
        self.productFam = ''
        self.productId = ''
        self.productVer = ''

    def getQue1Msg(self, value):
        """从MainLayout2获取Product Family Name信息"""
        self.productFam = value

    def getQue2Msg(self, value):
        """从MainLayout2获取Product ID, Ver信息"""
        try:
            self.productId, self.productVer = value.split(',')
        except ValueError:
            if value:
                self.productId = value
            else:
                self.productId = ''
                self.productVer = ''

    def getFunMsg(self, value):
        """从MainLayout2获取操作命令，并进行判断，将相应的数据传给TableWeiget"""
        tbname = 'psmc_product_version'
        item = ['PowerChip_Product_ID']
        productinfo = dict()
        productid = dict()
        df = pd.DataFrame()
        productinfo['Nick_Name'] = self.productFam
        productinfo['UniIC_Product_ID'] = self.productId
        productinfo['UniIC_Product_Version'] = self.productVer
        columns = list(productinfo.keys())
        for key in columns:
            if productinfo[key] == '':
                del productinfo[key]
        if value == 'Product Lot Check':
            """提供所有的Lot信息(包含已经在WH的产品)"""
            mysql = MySQL()
            mysql.selectDb('configdb')  # 连接数据库
            des, sql_result = mysql.fetchAll(tbname=tbname, items=item, condition=productinfo)
            mysql.cur.close()
            productid[''.join(des)] = sql_result    # 生成PowerChip_Product_Version List
            for i in productid[''.join(des)]:
                mysql = MySQL()
                mysql.selectDb('testdb')  # 连接数据库
                des, sql_result = mysql.fetchAll(tbname='psmc_lot_tracing_table', items='*', condition={'Current_Chip_Name': ''.join(i)})
                mysql.cur.close()
                df = df.append(pd.DataFrame(sql_result, columns=des), ignore_index=True)
            if not df.empty:
                df.sort_values(by='Forecast_Date', ascending=False, inplace=True)
                df = df.astype(str)
                for index, row in df.iterrows():    # 如果Qty 为0, 则将数据删除
                    if row['Qty'] == '0':
                        df.drop(index, inplace=True)
                df.replace(['nan', 'None'], '', inplace=True)
                df.replace('1.0', 'Y', inplace=True)
                self.model = PandasModel(df)
                self.TableWidget.setModel(self.model)

        # todo if value == 'Product Lot Check':
        #     pass
        # todo if value == 'Product Shipping Check':
        #     pass
        # todo if value == 'Product Q-Time Check':
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


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # main = WipTable()
    # main.productFam = 'Giulia'
    # main.productId = ''
    # main.productVer = ''
    # main.getFunMsg('Daily WIP Check')
    # main.show()
    # sys.exit(app.exec_())
    # main = WipTable()
    database = 'testdb'
    Current_Chip_Name = 'AAPS70D1D-0A01'
    ProductLotQuery(database=database, condition=Current_Chip_Name)   # Current_Chip_Name


