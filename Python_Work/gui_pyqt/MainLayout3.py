# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:${NAME}.py
# @Time:${DATE}${TIME}
# @Author:Jason_Yin

"""
生成mainlayout3 中所需要的table界面， 包括根据Product Query的响应函数，已执行相应的查询动作
"""

import sys
import math
import re
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from Python_Work.gui_pyqt.mysqlconfig import MySQL
from Python_Work.gui_pyqt.mysqliteconfig import TempTable


class WipTable(QWidget):
    def __init__(self):
        super(WipTable, self).__init__()

        # -----------------变量定义及初始化--------------
        self.TableWidget = None

        self.fab = ''
        self.productFam = ''
        self.productId = list()
        self.productVer = list()
        self.model = ''

        self.lot_df = pd.DataFrame()  # 要写入数据框的数据

        # -----------------UI定义----------------
        self.iniUI()

    def iniUI(self):

        # ----------------定义布局，控件-------------
        layout = QVBoxLayout()

        # --------------定义QtableView控件----------
        self.TableWidget = QTableView()

        # -------------设置Table的属性--------------
        # self.TableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)   # 表格禁止编辑
        # self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)   # 按行选择
        # self.TableWidget.setAlternatingRowColors(1)                  # 行间隔变色（boolen）
        # self.TableWidget.setSortingEnabled(True)

        layout.addWidget(self.TableWidget)

        self.setLayout(layout)

    def iniLocal(self):
        """用于初始化tableview中的数据"""
        self.fab = list()
        self.productFam = list()
        self.productId = list()
        self.productVer = list()
        self.model = ''

        self.lot_df = pd.DataFrame()    # 要写入数据框的数据

    def getQue1Msg(self, value):
        """从MainLayout2获取Product Family Name信息"""
        self.productFam = [value]

    def getQue2Msg(self, value1, value2):
        """从MainLayout2获取Product ID, Ver信息，如果product id和ver无法分裂，则有两种情况，只输入product id, 或什么都没输入"""
        self.fab = [value1]
        prodVerreg1 = re.compile(r'\[[A-Za-z0-9_.*+%!()\-]*,V\d*\]')
        prodVerreg2 = re.compile(r'\[V\d*\]')
        if value2 is None:
            pass
        elif re.findall(prodVerreg1, value2):
            for i in re.findall(prodVerreg1, value2):
                self.productId.append(i.strip('[|]').split(',')[0])
                self.productVer.append(i.strip('[|]').split(',')[1])
            self.productId = list(set(self.productId))
            self.productVer = list(set(self.productVer))
        elif re.findall(prodVerreg2, value2):
            for i in re.findall(prodVerreg2, value2):
                self.productVer.append(i.strip('[|]'))
            self.productId = ['']
        else:
            for i in value2.split('],['):
                self.productId.append(i.strip('[|]'))
            self.productVer = ['']

    def getFunMsg(self, value):  # Value为点击功能的项目
        """从MainLayout2获取操作命令，并进行判断，将相应的数据传给TableWeiget"""
        productinfo = dict()
        # 获取参数
        productinfo['Nick_Name'] = self.productFam
        productinfo['Fab'] = self.fab
        productinfo['UniIC_Product_ID'] = self.productId
        productinfo['UniIC_Product_Version'] = self.productVer

        columns = list(productinfo.keys())  # 获取参数名['Nick_Name','Fab','UniIC_Product_ID','UniIC_Product_Version']
        for key in columns:                 # 如果参数为空，则去掉该参数
            if productinfo[key] == ['']:
                del productinfo[key]
        productid = GetProductId(productinfo)  # 输入产品信息，生成PowerChip_Product_Version List字典
        if value == 'Daily WIP Check':
            """返回查询当前时间最新的Lot状态"""
            self.lot_df = DailyWipCheck(productid, productinfo['Fab'])
            mytable = TempTable(self.lot_df)   # 将查询的结果写入sqlite数据库(tempdb)
            self.TableWidget.setModel(mytable.model)
            layout.addWidget(self.TableWidget)





            # self.model = PandasModel(self.lot_df)
            # self.TableWidget.setModel(self.model)

        elif value == 'Product Lot Check':
            """返回所有的Lot的信息最终状态(包含已经在WH的产品)"""
            self.lot_df = ProductLotCheck(productid, productinfo['Fab'])
            self.mydatagird.totalPage = math.ceil(self.mydatagird.totalRecordCoutn / self.mydatagird.pageRecordCount)
        #
        #     self.mydatagird.switchPage.setText("当前%s/%s页" % (self.mydatagird.currentPage, self.mydatagird.totalPage))
        #     self.model = PandasModel(self.lot_df)
        #     self.TableWidget.setModel(self.model)
        #
        # elif value == 'Product Q-Time Check':
        #     """返回所有的未发货，但是已经到WH的Lot，并Hight Light大约>60天的Lot"""
        #     self.lot_df = ProductQCheck(psmc_productid)


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
    product = []
    proinfo = productinfo.copy()
    tbname = '%s_product_version' % ''.join(proinfo['Fab']).lower()
    item = ['%s_Product_ID' % ''.join(proinfo['Fab'])]
    del proinfo['Fab']
    # ---- 在数据库中查询数据 ----
    mysql = MySQL()
    mysql.selectDb('configdb')  # 连接数据库
    psmc_des, psmc_sql_res = mysql.fetchAll(tbname=tbname, items=item, condition=proinfo)
    mysql.cur.close()
    for i in range(len(psmc_sql_res)):
        product.append(''.join(psmc_sql_res[i]))
    psmc_productid[''.join(psmc_des)] = product
    return psmc_productid


def ProductLotCheck(psmc_productid, targetpage, pagesize):
    """如果点击Lot Check, 则根据输入的PowerChip_Product_Version List字典返回查询的数据结果"""
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    lotche_des, lotche_sql_res = mysql.fetchAll(tbname='psmc_lot_tracing_table', page=targetpage, size=pagesize, items='*', condition={'Current_Chip_Name': psmc_productid['psmc_Product_ID']})
    mysql.cur.close()
    lot_df = pd.DataFrame(lotche_sql_res, columns=lotche_des)

    if not lot_df.empty:  # 如果数据非空，则将数据转化为字符，并用None替换空，Y替换Wafer
        lot_df = lot_df.astype(str)
        lot_df.replace(['nan', 'None'], '', inplace=True)
        lot_df.replace('1.0', 'Y', inplace=True)
    else:
        totalpage = 0
    return totalpage, lot_df


def DailyWipCheck(productid, Fab):
    """通过查询当前数据库中最新的时间，根据时间反差当前Lot的信息"""
    # ---- 变量定义----
    set_time = dict()
    lot_df = pd.DataFrame()

    set_time['Fab'] = Fab
    tbname = '{}_lot_tracing_table'.format(set_time['Fab'][0].lower())

    # ---- 连接数据库 ----
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    time_des, time_sql_res = mysql.fetchAll(tbname=tbname, items=['Current_Time'])
    time_df = pd.DataFrame(time_sql_res, columns=time_des)  # 生成current_time的dataframe
    time_df.sort_values(by='Current_Time', ascending=False, inplace=True)
    set_time['Current_Time'] = [time_df.iat[0, 0].date()]  # iat基于索引位置的选择方法
    set_time['Current_Chip_Name'] = productid['{}_Product_ID'.format(set_time['Fab'][0])]  # 将Current_Chip_Name加入setting time字典，用于sql的筛选条件

    # ---- 连接数据库查询 ----
    mysql.selectDb('testdb')  # 连接数据库
    _sql = "a.Current_Chip_Name = '" + "' OR a.Current_Chip_Name= '".join(set_time['Current_Chip_Name']) + "'"
    sqlquery = """Select a.Wafer_Start_Date, a.MLot_ID, a.Lot_ID, b.UniIC_Product_ID, b.UniIC_Product_Version, a.Fab, a.Stage, DATE_FORMAT(a.Current_Time, '%Y-%m-%d') AS 'Current_Time',
        a.Forecast_Date, a.Qty, a.`#01`, a.`#02`, a.`#03`, a.`#04`, a.`#05`, a.`#06`, a.`#07`, a.`#08`, a.`#09`, a.`#10`, a.`#11`, a.`#12`, a.`#13`, a.`#14`, a.`#15`, a.`#16`, a.`#17`, a.`#18`,
        a.`#19`, a.`#20`, a.`#21`, a.`#22`, a.`#23`, a.`#24`, a.`#25` FROM testdb.`{0}_lot_tracing_table` AS a JOIN configdb.`{0}_product_version` AS b on
        a.Current_Chip_Name = b.{1}_Product_ID WHERE ({2}) and (DATE_FORMAT(a.Current_Time, '%Y-%m-%d') = '{3}')""".format(
        set_time['Fab'][0].lower(), set_time['Fab'][0], _sql, set_time['Current_Time'][0])
    lotche_des, lotche_sql_res = mysql.sqlAll(sqlquery)
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


