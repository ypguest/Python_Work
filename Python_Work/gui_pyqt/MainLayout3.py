#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
生成mainlayout3 中所需要的table界面， 包括根据Product Query的响应函数，已执行相应的查询动作
"""

import sys
import math
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Python_Work.gui_pyqt.mysqlconfig import MySQL
from Python_Work.gui_pyqt.DataGrid import DataGrid


pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


class WipTable(QWidget):
    def __init__(self):
        super(WipTable, self).__init__()

        # -----------------变量定义及初始化--------------
        self.TableWidget = None
        self.mydatagird = None

        self.productFam = ''
        self.productId = ''
        self.productVer = ''
        self.model = ''

        self.lot_df = pd.DataFrame()
        # -----------------UI定义----------------
        self.iniUI()

    def iniUI(self):

        # ----------------定义布局，控件-------------
        layout = QVBoxLayout()

        # --------------定义QtableView控件----------
        self.TableWidget = QTableView()

        # -------------设置Table的属性--------------
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 表格禁止编辑
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)   # 按行选择
        self.TableWidget.setAlternatingRowColors(1)                  # 行间隔变色（boolen）

        layout.addWidget(self.TableWidget)

        # ------------设置DataGride---------------
        self.mydatagird = DataGrid()
        self.mydatagird.prevButton.clicked.connect(self.onPrevButtonClick)
        self.mydatagird.nextButton.clicked.connect(self.onNextButtonClick)
        layout.addWidget(self.mydatagird)

        self.setLayout(layout)

    def onPrevButtonClick(self):
        print(self.lot_df)

    def onNextButtonClick(self):
        print("""on PREV""")

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
        productinfo = dict()
        # 获取参数
        productinfo['Nick_Name'] = self.productFam
        productinfo['UniIC_Product_ID'] = self.productId
        productinfo['UniIC_Product_Version'] = self.productVer

        columns = list(productinfo.keys())  # 获取参数名['Nick_Name','UniIC_Product_ID','UniIC_Product_Version']
        for key in columns:                 # 如果参数为空，则去掉该参数
            if productinfo[key] == '':
                del productinfo[key]
        psmc_productid = GetProductId(productinfo)  # 输入产品信息，生成PowerChip_Product_Version List字典
        if value == 'Daily WIP Check':
            """返回查询当前时间最新的Lot状态"""

            self.lot_df = DailyWipCheck(psmc_productid)

            self.mydatagird.totalRecordCoutn = self.lot_df.shape[0]
            self.mydatagird.totalPage = math.ceil(self.mydatagird.totalRecordCoutn / self.mydatagird.PageRecordCount)
            self.mydatagird.switchPage.setText("当前%s/%s页" % (self.mydatagird.currentPage, self.mydatagird.totalPage))

            self.model = PandasModel(self.lot_df)
            self.TableWidget.setModel(self.model)

        elif value == 'Product Lot Check':
            """返回所有的Lot的信息最终状态(包含已经在WH的产品)"""
            self.lot_df = ProductLotCheck(psmc_productid)

            # totalrow = self.lot_df.shape[0]
            # self.mydatagird.totalRecordCoutn = self.lot_df.shape[0]
            # self.mydatagird.totalPage = math.ceil(self.mydatagird.totalRecordCoutn / self.mydatagird.PageRecordCount)
            # self.mydatagird.switchPage.setText("当前%s/%s页" % (self.mydatagird.currentPage, self.mydatagird.totalPage))
            self.model = PandasModel(self.lot_df)
            self.TableWidget.setModel(self.model)



        elif value == 'Product Q-Time Check':
            """返回所有的未发货，但是已经到WH的Lot，并Hight Light大约>60天的Lot"""
            self.lot_df = ProductQCheck(psmc_productid)





def ProductQCheck(psmc_productid):
    """返回所有的未发货，但是已经到WH的Lot，并Hight Light大约>60天的Lot"""
    set_time = dict()
    lot_df = pd.DataFrame()
    time_df = pd.DataFrame()
    # todo 未做完
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    time_des, time_sql_res = mysql.fetchAll(tbname='psmc_lot_tracing_table', items=['Current_Time'])
    time_df = time_df.append(pd.DataFrame(time_sql_res, columns=time_des), ignore_index=True)  # 生成current_time的datafr
    time_df.sort_values(by='Current_Time', ascending=False, inplace=True)
    mysql.cur.close()
    set_time['Current_Time'] = time_df.iat[0, 0]
    return lot_df


def GetProductId(productinfo):
    """输入产品信息，生成PowerChip_Product_Version List字典"""
    psmc_productid = dict()
    tbname = 'psmc_product_version'
    item = ['PowerChip_Product_ID']
    mysql = MySQL()
    mysql.selectDb('configdb')  # 连接数据库
    psmc_des, psmc_sql_res = mysql.fetchAll(tbname=tbname, items=item, condition=productinfo)
    mysql.cur.close()
    psmc_productid[''.join(psmc_des)] = psmc_sql_res
    return psmc_productid


def ProductLotCheck(psmc_productid):
    """如果点击Lot Check, 则根据输入的PowerChip_Product_Version List字典返回查询的数据结果"""
    lot_df = pd.DataFrame()
    for i in psmc_productid['PowerChip_Product_ID']:  # 遍历psmc_product_id
        mysql = MySQL()
        mysql.selectDb('testdb')  # 连接数据库
        lotche_des, lotche_sql_res = mysql.fetchAll(tbname='psmc_lot_tracing_table', items='*', condition={'Current_Chip_Name': ''.join(i)})  # 获取lot,
        mysql.cur.close()
        lot_df = lot_df.append(pd.DataFrame(lotche_sql_res, columns=lotche_des), ignore_index=True)
    if not lot_df.empty:  # 对获取query的结果按照Forecast_Date排序
        lot_df.sort_values(by='Forecast_Date', ascending=False, inplace=True)
        lot_df = lot_df.astype(str)
        for index, row in lot_df.iterrows():  # 如果Qty 为0, 则将数据删除
            if row['Qty'] == '0':
                lot_df.drop(index, inplace=True)
        lot_df.replace(['nan', 'None'], '', inplace=True)
        lot_df.replace('1.0', 'Y', inplace=True)
    else:
        pass
    return lot_df


def DailyWipCheck(psmc_productid):
    """通过查询当前数据库中最新的时间，根据时间反差当前Lot的信息"""
    # 变量定义
    set_time = dict()
    lot_df = pd.DataFrame()
    time_df = pd.DataFrame()

    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    time_des, time_sql_res = mysql.fetchAll(tbname='psmc_lot_tracing_table', items=['Current_Time'])
    time_df = time_df.append(pd.DataFrame(time_sql_res, columns=time_des), ignore_index=True)  # 生成current_time的datafr
    time_df.sort_values(by='Current_Time', ascending=False, inplace=True)
    mysql.cur.close()
    set_time['Current_Time'] = time_df.iat[0, 0]

    for i in psmc_productid['PowerChip_Product_ID']:
        set_time['Current_Chip_Name'] = ''.join(i)  # 将Current_Chip_Name加入setting time字典，用于sql的筛选条件
        mysql = MySQL()
        mysql.selectDb('testdb')  # 连接数据库
        lotche_des, lotche_sql_res = mysql.fetchAll(tbname='psmc_lot_tracing_table', items='*', condition=set_time)
        mysql.cur.close()
        lot_df = lot_df.append(pd.DataFrame(lotche_sql_res, columns=lotche_des), ignore_index=True)

    if not lot_df.empty:
        lot_df.sort_values(by='Forecast_Date', ascending=False, inplace=True)  # 按时间排序
        lot_df = lot_df.astype(str)  # 转换为字符
        for index, row in lot_df.iterrows():  # 如果Qty 为0, 则将数据删除
            if row['Qty'] == '0':
                lot_df.drop(index, inplace=True)
        lot_df.replace(['nan', 'None'], '', inplace=True)
        lot_df.replace('1.0', 'Y', inplace=True)
    else:
        pass
    return lot_df


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
    app = QApplication(sys.argv)
    main = WipTable()
    main.show()
    sys.exit(app.exec_())

    # main = WipTable()

    # database = 'testdb'
    # Current_Chip_Name = 'AAPS70D1D-0A01'
    # ProductLotQuery(database=database, condition=Current_Chip_Name)   # Current_Chip_Name


