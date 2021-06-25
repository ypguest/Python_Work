# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3
import random
import pandas as pd
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplcursors

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.gridspec import GridSpec
from matplotlib.dates import DateFormatter, MonthLocator, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.widgets import Button, RadioButtons, Button


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel

from my_SqlConfig import MySQL, MySQLite
from my_MatplotlibSet import MyLineSet

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行

# # plt设置
plt.style.use('seaborn-whitegrid')    # R语言风格


class QTabDataGrid(QWidget):

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
        super(QTabDataGrid, self).__init__()
        # ==== 设置QSqlTableModel模型 ====
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/database.db')
        # ==== 创建QSqlTableModel ====
        self.queryModel = QSqlTableModel()
        self.queryModel.setTable('tempdb')
        self.queryModel.select()
        db.close()
        # ==== 设置QSqlTableModel排序 ====
        self.queryModel.setEditStrategy(QSqlTableModel.OnFieldChange)    # 所有变更实时更新到数据库中
        self.proxyModel = QSortFilterProxyModel()     # 通过代理模型增加排序功能
        self.proxyModel.setFilterKeyColumn(0)
        self.proxyModel = QSortFilterProxyModel()     # 通过代理模型增加排序功能
        self.proxyModel.setSourceModel(self.queryModel)   # 将筛选模型赋给Sqltable模型
        # ==== 设置表格属性 ====
        self.tableView = QTableView()     # 创建表格
        self.tableView.setModel(self.proxyModel)    # 将模型绑定
        self.tableView.verticalHeader().setVisible(False)    # 隐藏行名称
        self.tableView.setSortingEnabled(True)    # 启用排序功能
        # ==== 表头设置 ====
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)   # 表示均匀拉直表头
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        # self.tableView.setItemDelegateForColumn(2, EmptyDelegate(self))
        # ==== 将tableView部署 ====
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.tableView)
        self.setLayout(mainLayout)


class QMapDataGridWip(QMainWindow):
    """针对wip数据生成当前的wip图"""
    def __init__(self, fab, db):
        super().__init__()   # 调用父类构造函数
        mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']    # 汉字字体
        mpl.rcParams['font.size'] = 8   # 字体大小
        mpl.rcParams['axes.unicode_minus'] = False    # 正常显示符号
        self.fab = fab
        self.db = db
        self.__iniFigure()    # 创建绘图系统，初始化窗口
        self.__drawFigure()   # 绘图

    # ==========自定义函数=================
    def __iniFigure(self, width=11, height=5, dpi=100):
        """ 创建绘图系统，初始化窗口 """
        self.__fig = Figure(figsize=(width, height), dpi=dpi)   # 创建图板
        self.__fig.suptitle("{} Daily Wip Information" .format(self.fab))  # 总的图标题

        figCanvas = FigureCanvas(self.__fig)  # 创建FigureCanvas对象，必须传递一个Figure对象
        naviToolbar = NavigationToolbar(figCanvas, self)  # 创建工具栏
        naviToolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置工具栏注释位置

        self.addToolBar(naviToolbar)  # 添加工具栏到主窗口
        self.setCentralWidget(figCanvas)

    def __getdata(self):
        """ 根据工厂wip信息，获取数据库中的数据，并进行统计 """
        _mysql = MySQLite()
        _desc, _result = _mysql.fetchAll(self.db)   # 从本地SQLite数据库中获取暂存的查询数据
        _wip_df = pd.DataFrame(_result, columns=_desc)

        # ==== 按type生成产品信息，按wip type生成layer信息 ====
        self._wip_layer_df = dict()   # 按type分类wip信息

        if self.fab == 'XMC':
            self.wip_types = ['logic', 'dram', '3DIC']
            for wip_type in self.wip_types:
                # ==== 按process 类型对wip进行分类 ====
                data_wip = _wip_df[_wip_df['UniIC_Product_ID'].str.contains(wip_type)].copy()
                data_wip['Qty'] = data_wip['Qty'].apply(pd.to_numeric, errors='coerce')  # 将Qty转变为数字
                data_wip['Stage'] = data_wip['Stage'].str.upper()    # 将Stage转换为大写

                # ==== 获取layer信息, 并将wip按layer求和 ====
                mysql_layer = MySQL()
                mysql_layer.selectDb(database='product_layer')
                desc_layer, result_layer = mysql_layer.sqlAll('SELECT * FROM {}_{}_layer'.format(self.fab.lower(), wip_type.lower()))
                layer_infor = pd.DataFrame(result_layer, columns=desc_layer)
                data_wip = pd.merge(data_wip, layer_infor, how='left', on='Stage')
                grouped_data = data_wip.groupby(['Layer'])['Qty'].sum()

                # ==== 将layer与求和结果进行合并，并删除无用信息 ====
                layer_infor.drop_duplicates(subset=['Layer'], keep='first', inplace=True)
                layer_infor.set_index(["Seq"], inplace=True)
                del layer_infor['Index'], layer_infor['Stage']
                # ==== 生成用于作图的数据 ====
                self._wip_layer_df[wip_type] = pd.merge(layer_infor, grouped_data, how='left', left_on='Layer', right_index=True).fillna(0)
        if self.fab == 'PSMC':
            self.wip_types = ['dram']
            for wip_type in self.wip_types:
                data_wip = _wip_df.copy()
                data_wip['Qty'] = data_wip['Qty'].apply(pd.to_numeric, errors='coerce')
                data_wip['Stage'] = data_wip['Stage'].str.upper()
                # ==== 获取layer信息, 并将wip按layer求和 ====
                mysql_layer = MySQL()
                mysql_layer.selectDb(database='product_layer')
                desc_layer, result_layer = mysql_layer.sqlAll('SELECT * FROM {}_{}_layer'.format(self.fab.lower(), wip_type.lower()))
                layer_infor = pd.DataFrame(result_layer, columns=desc_layer)
                data_wip = pd.merge(data_wip, layer_infor, how='left', on='Stage')
                grouped_data = data_wip.groupby(['Layer'])['Qty'].sum()
                # ==== 将layer与求和结果进行合并，并删除无用信息 ====
                layer_infor.drop_duplicates(subset=['Layer'], keep='first', inplace=True)
                layer_infor.set_index(["Seq"], inplace=True)
                del layer_infor['Index'], layer_infor['Stage']
                # ==== 生成用于作图的数据 ====
                self._wip_layer_df[wip_type] = pd.merge(layer_infor, grouped_data, how='left', left_on='Layer', right_index=True).fillna(0)

    def __drawFigure(self):  # 绘图

        self.__getdata()   # 获取数据self._wip_layer_df

        if self.fab == 'XMC':
            # 所需变量设置
            _ax = list()
            _loc_ax = list()
            i = 0

            # 设置axes的长，宽
            _grid = self.__fig.add_gridspec(2, 16)
            _loc_ax.append([0, 1, 0, 13])
            _loc_ax.append([1, 2, 12, 13])
            _loc_ax.append([0, 2, 14, 16])

            for wip_type in self._wip_layer_df:
                _layername = self._wip_layer_df[wip_type]['Layer']   # 参数1
                _count = self._wip_layer_df[wip_type]['Qty']  # 参数2
                _ax.append(self.__fig.add_subplot(_grid[_loc_ax[i][0]:_loc_ax[i][1], _loc_ax[i][2]:_loc_ax[i][3]]))
                _ax[i].bar(_layername,  _count, width=0.4)
                _ax[i].set_xlim(-1, len(_layername))
                _ax[i].set_ylim(0, 1000)
                for tick in _ax[i].get_xticklabels():
                    tick.set_rotation(90)
                i = i + 1
        if self.fab == 'PSMC':
            _ax = list()
            _loc_ax = list()
            i = 0

            # 设置axes的长，宽
            _grid = self.__fig.add_gridspec(16, 16)
            _loc_ax.append([0, 16, 0, 16])

            for wip_type in self._wip_layer_df:
                _layername = self._wip_layer_df[wip_type]['Layer']   # 参数1
                _count = self._wip_layer_df[wip_type]['Qty']  # 参数2
                _ax.append(self.__fig.add_subplot(_grid[_loc_ax[i][0]:_loc_ax[i][1], _loc_ax[i][2]:_loc_ax[i][3]]))
                _ax[i].bar(_layername,  _count, width=0.4)
                _ax[i].set_xlim(-1, len(_layername))
                _ax[i].set_ylim(0, 1000)
                _ax[i].tick_params(axis='x', rotation=90)
                i = i + 1


class QMapDataGridHis(QMainWindow):
    """针对lot history的数据转换为图"""
    def __init__(self, db):
        super().__init__()  # 调用父类构造函数

        mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']  # 汉字字体
        mpl.rcParams['font.size'] = 8  # 字体大小
        mpl.rcParams['axes.unicode_minus'] = False  # 正常显示符号

        self.fab = None   # 定义变量self.fab
        self.db = db      # 定义变量self.db

        self.__iniFigure()  # 创建绘图系统，初始化窗口
        self.__getdata()    # 获取数据
        self.__drawFigure()  # 绘图

    # ==========自定义函数=================
    def __iniFigure(self, width=11, height=5, dpi=100):
        """ 创建绘图系统，初始化窗口 """
        self.__fig = Figure(figsize=(width, height), dpi=dpi)   # 创建图板

        figCanvas = FigureCanvas(self.__fig)  # 创建FigureCanvas对象，必须传递一个Figure对象
        naviToolbar = NavigationToolbar(figCanvas, self)  # 创建工具栏
        naviToolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置工具栏注释位置

        self.addToolBar(naviToolbar)  # 添加工具栏到主窗口
        self.setCentralWidget(figCanvas)   # 将画布设置为中心控件

    def __getdata(self):
        """ 获取数据库中的lothistory数据，并根据工厂信息返回涉及到的wip, layer，产品信息"""
        """
        1. 通过P2,P3-> PSMC, P10-> XMC判断出涉及的工厂
        2. 并将该信息按照工厂分别返回与wip数据进行合并，返回self._his_wip_df 和self._layer_df数据
        """
        self._product_infor = pd.DataFrame()   # 返回涉及的产品信息；
        self._his_wip_df = dict()  # 按type分类wip信息；
        self._layer_df = dict()   # 按type分类layer信息；

        _desc_layer = dict()   # 定义layer的字典，用于存储不同工厂的layer
        _result_layer = dict()

        # ========= 连接数据库，用于查询layer, 产品的版本 ===========
        _mysql_pro = MySQL()
        _mysql_pro.selectDb('configdb')
        _mysql_layer = MySQL()
        _mysql_layer.selectDb('product_layer')

        _mysql = MySQLite()   # 获取self.db中的数据
        _desc, _result = _mysql.fetchAll(self.db)
        _wip_df = pd.DataFrame(_result, columns=_desc)
        _order = ['MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'UniIC_Product_ID', 'UniIC_Product_Version', 'Seq', 'layer', 'Stage', 'Current_Time', 'Qty',
                  '#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                  '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20',
                  '#21', '#22', '#23', '#24', '#25']

        # ========= 根据涉及的Fab名称判断画图的方式, 并将wip信息放入self._his_wip_df ======================
        _fablist = _wip_df['Fab'].tolist()    # 得到Fab信息
        _product_chip_name = _wip_df['Current_Chip_Name'].unique()  # 提取出该Lot涉及的product信息

        if (('P2' in _fablist) or ('P3' in _fablist)) and ('P10' not in _fablist):
            self.fab = 'PSMC'
            self._his_wip_df['PSMC'] = dict()
            _wip_data = _wip_df[_wip_df.Fab.isin(['P2', 'P3'])]
            _wip_data['Current_Time'] = pd.to_datetime(_wip_data['Current_Time'], format='%Y/%m/%d %H:%M:%S')  # 转换为时间格式
            _wip_data['Stage'] = _wip_data['Stage'].str.upper()
            del (_wip_data['Wafer_Start_Date'], _wip_data['Index'], _wip_data['Fab'], _wip_data['Layer'], _wip_data['Forecast_Date'])

            # ========== 获得该Lot所涉及到的产品信息, self._product_infor名称 ==========
            _desc_pro, _result_pro = _mysql_pro.fetchAll(tbname='psmc_product_version', items=['PSMC_Product_ID', 'UniIC_Product_ID', 'UniIC_Product_Version'], condition=({'PSMC_Product_ID': _product_chip_name}))
            self._product_infor = pd.DataFrame(_result_pro, columns=_desc_pro)
            self._product_infor.rename(columns={'PSMC_Product_ID': 'Fab_Product_ID'}, inplace=True)
            # ========== 获取layer信息 ==========
            _desc_layer['psmc_dram'], _result_layer['psmc_dram'] = _mysql_layer.fetchAll(tbname='psmc_dram_layer', items=['layer', 'Stage', 'Seq'])
            self._layer_df['psmc_dram'] = pd.DataFrame(_result_layer['psmc_dram'], columns=_desc_layer['psmc_dram'])

            # ========== 将相关信息匹配至self._his_wip_df, 并得到'MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'UniIC_Product_ID', 'UniIC_Product_Version', 'Seq', 'layer', 'Stage', 'Current_Time', 'Qty' ===========
            _wip_data = pd.merge(_wip_data, self._product_infor, left_on='Current_Chip_Name', right_on='Fab_Product_ID')
            _wip_data = pd.merge(_wip_data, self._layer_df['psmc_dram'], left_on='Stage', right_on='Stage').sort_values(by='Current_Time', axis=0, ascending=True, inplace=False)
            self._his_wip_df['PSMC']['psmc_dram'] = _wip_data[_order]

        if ('P10' in _fablist) and ('P2' not in _fablist) and ('P3' not in _fablist):
            self.fab = 'XMC'
            self._his_wip_df['XMC'] = dict()
            _wip_data = _wip_df[_wip_df.Fab.isin(['P10'])]  # 获取wip信息
            _wip_data['Current_Time'] = pd.to_datetime(_wip_data['Current_Time'], format='%Y/%m/%d %H:%M:%S')  # 转换为时间格式
            _wip_data['Stage'] = _wip_data['Stage'].str.upper()
            del (_wip_data['Wafer_Start_Date'], _wip_data['Index'], _wip_data['Fab'], _wip_data['Layer'], _wip_data['Forecast_Date'])

            # ========== 获得该Lot所涉及到的产品信息，self._product_infor名称 =========
            _desc_pro, _result_pro = _mysql_pro.fetchAll(tbname='xmc_product_version', items=['XMC_Product_ID', 'UniIC_Product_ID', 'UniIC_Product_Version'], condition=({'XMC_Product_ID': _product_chip_name}))
            self._product_infor = pd.DataFrame(_result_pro, columns=_desc_pro)
            self._product_infor.rename(columns={'XMC_Product_ID': 'Fab_Product_ID'}, inplace=True)  # 改名
            # ========== 获取layer信息 ==========
            _desc_layer['xmc_3dic'], _result_layer['xmc_3dic'] = _mysql_layer.fetchAll(tbname='xmc_3dic_layer', items=['layer', 'Stage', 'Seq'])
            _desc_layer['xmc_dram'], _result_layer['xmc_dram'] = _mysql_layer.fetchAll(tbname='xmc_dram_layer', items=['layer', 'Stage', 'Seq'])
            _desc_layer['xmc_logic'], _result_layer['xmc_logic'] = _mysql_layer.fetchAll(tbname='xmc_logic_layer', items=['layer', 'Stage', 'Seq'])
            self._layer_df['xmc_3dic'] = pd.DataFrame(_result_layer['xmc_3dic'], columns=_desc_layer['xmc_3dic'])
            self._layer_df['xmc_dram'] = pd.DataFrame(_result_layer['xmc_dram'], columns=_desc_layer['xmc_dram'])
            self._layer_df['xmc_logic'] = pd.DataFrame(_result_layer['xmc_logic'], columns=_desc_layer['xmc_logic'])

            # ========== 将相关信息匹配至self._his_wip_df ===========
            _wip_data = pd.merge(_wip_data, self._product_infor, left_on='Current_Chip_Name', right_on='Fab_Product_ID')

            self._his_wip_df['XMC']['xmc_3dic'] = pd.merge(_wip_data, self._layer_df['xmc_3dic'], left_on='Stage', right_on='Stage').sort_values(by='Current_Time', axis=0, ascending=True, inplace=False)[_order]
            self._his_wip_df['XMC']['xmc_dram'] = pd.merge(_wip_data, self._layer_df['xmc_dram'], left_on='Stage', right_on='Stage').sort_values(by='Current_Time', axis=0, ascending=True, inplace=False)[_order]
            self._his_wip_df['XMC']['xmc_logic'] = pd.merge(_wip_data, self._layer_df['xmc_logic'], left_on='Stage', right_on='Stage').sort_values(by='Current_Time', axis=0, ascending=True, inplace=False)[_order]

        if (('P2' in _fablist) or ('P3' in _fablist)) and ('P10' in _fablist):
            self.fab = ['PSMC', 'XMC']
            self._his_wip_df['PSMC'] = _wip_df[_wip_df.Fab.isin(['P2', 'P3'])]
            del (self._his_wip_df['PSMC']['Wafer_Start_Date'], self._his_wip_df['PSMC']['Index'], self._his_wip_df['PSMC']['Fab'], self._his_wip_df['PSMC']['Layer'], self._his_wip_df['PSMC']['Forecast_Date'])
            self._his_wip_df['XMC'] = _wip_df[_wip_df.Fab.isin(['P10'])]
            del (self._his_wip_df['XMC']['Wafer_Start_Date'], self._his_wip_df['XMC']['Index'], self._his_wip_df['XMC']['Fab'], self._his_wip_df['XMC']['Layer'], self._his_wip_df['XMC']['Forecast_Date'])
            # ========== 获得该Lot所涉及到的产品信息，self._product_infor名称 ==========
            _desc_pro_xmc, _result_pro_xmc = _mysql_pro.fetchAll(tbname='xmc_product_version', items=['XMC_Product_ID', 'UniIC_Product_ID', 'UniIC_Product_Version'], condition=({'XMC_Product_ID': _product_chip_name}))
            _product_infor_xmc = pd.DataFrame(_result_pro_xmc, columns=_desc_pro_xmc)  # 获得该Lot所涉及到的layer库名称
            _product_infor_xmc.rename(columns={'XMC_Product_ID': 'Fab_Product_ID'}, inplace=True)
            _desc_pro_psmc, _result_pro_psmc = _mysql_pro.fetchAll(tbname='psmc_product_version', items=['PSMC_Product_ID', 'UniIC_Product_ID', 'UniIC_Product_Version'], condition=({'PSMC_Product_ID': _product_chip_name}))
            _product_infor_psmc = pd.DataFrame(_result_pro_psmc, columns=_desc_pro_psmc)  # 获得该Lot所涉及到的layer库名称
            _product_infor_psmc.rename(columns={'PSMC_Product_ID': 'Fab_Product_ID'}, inplace=True)
            self._product_infor = pd.concat([_product_infor_xmc, _product_infor_psmc], axis=0, join='inner')
            # ========== 获取layer信息 ==========
            _desc_layer['xmc_3dic'], _result_layer['xmc_3dic'] = _mysql_layer.fetchAll(tbname='xmc_3dic_layer', items=['layer', 'Stage', 'Seq'])
            _desc_layer['xmc_dram'], _result_layer['xmc_dram'] = _mysql_layer.fetchAll(tbname='xmc_dram_layer', items=['layer', 'Stage', 'Seq'])
            _desc_layer['xmc_logic'], _result_layer['xmc_logic'] = _mysql_layer.fetchAll(tbname='xmc_logic_layer', items=['layer', 'Stage', 'Seq'])
            _desc_layer['psmc_dram'], _result_layer['psmc_dram'] = _mysql_layer.fetchAll(tbname='psmc_dram_layer', items=['layer', 'Stage', 'Seq'])

            self._layer_df['xmc_3dic'] = pd.DataFrame(_result_layer['xmc_3dic'], columns=_desc_layer['xmc_3dic'])
            self._layer_df['xmc_dram'] = pd.DataFrame(_result_layer['xmc_dram'], columns=_desc_layer['xmc_dram'])
            self._layer_df['xmc_logic'] = pd.DataFrame(_result_layer['xmc_logic'], columns=_desc_layer['xmc_logic'])
            self._layer_df['psmc_dram'] = pd.DataFrame(_result_layer['psmc_dram'], columns=_desc_layer['psmc_dram'])

            self._his_wip_df['XMC'] = pd.merge(self._his_wip_df['XMC'], self._product_infor, left_on='Current_Chip_Name', right_on='Fab_Product_ID')
            self._his_wip_df['XMC']['Stage'].str.upper()
            self._his_wip_df['XMC'] = self._his_wip_df['XMC'][_order]
            self._his_wip_df['PSMC'] = pd.merge(self._his_wip_df['PSMC'], self._product_infor, left_on='Current_Chip_Name', right_on='Fab_Product_ID')
            self._his_wip_df['PSMC']['Stage'].str.upper()
            self._his_wip_df['PSMC'] = self._his_wip_df['PSMC'][_order]

    def __drawFigure(self):

        alldays = DayLocator()
        mondays = WeekdayLocator(MONDAY)
        mondayFormatter = DateFormatter('%Y-%m-%d')
        # ========== 根据Lot id返回lot histroy相关信息 ==========
        for fab, _wip_data in self._his_wip_df.items():
            if fab == 'PSMC':
                # ========== 初始化子图 ==========
                self.__fig.suptitle("{} Lot History Trend".format(fab))  # 总的图标题
                ax = self.__fig.add_axes([0.05, 0.15, 0.93, 0.78])

                xmax = _wip_data['psmc_dram']['Current_Time'].max()
                xmin = _wip_data['psmc_dram']['Current_Time'].min()
                Mlots_id = _wip_data['psmc_dram']['MLot_ID'].unique()     # 获取Mother Lot Id的list
                lots_id = _wip_data['psmc_dram']['Lot_ID'].unique()       # 获取Children Lot Id的list

                # ========== 生成layer，并根据layer生成Y坐标轴 ===========
                product_layer_list = self._layer_df['psmc_dram'].drop_duplicates(subset='layer', keep='first', inplace=False)[['layer', 'Seq']]
                product_layer_name = product_layer_list['layer'].tolist()
                product_layer_num = product_layer_list['Seq'].tolist()

                ax.axes.set_yticks(product_layer_num)
                ax.axes.set_yticklabels(product_layer_name)
                ax.yaxis.set_major_locator(MultipleLocator(1))

                for Mlot_id in Mlots_id:
                    datas = _wip_data['psmc_dram'][(_wip_data['psmc_dram']['MLot_ID'] == Mlot_id)].copy()
                    for lot_id in lots_id:
                        new_data = datas[(datas['Lot_ID'] == lot_id)].copy()
                        lines = ax.plot(new_data['Current_Time'], new_data['Seq'], linestyle='-', linewidth=1, label=lot_id)
                        mplcursors.cursor(lines)   # xxxxxxxxxxx
                        ax.xaxis.set_major_locator(mondays)
                        ax.xaxis.set_minor_locator(alldays)
                        ax.xaxis.set_major_formatter(mondayFormatter)
                        for tick in ax.get_xticklabels():
                            tick.set_rotation(90)
                            tick.set_horizontalalignment('center')

                ax.set_xlim(xmin, xmax)
                ax.set_ylim(0, len(product_layer_name) + 1)

            if fab == 'XMC':

                self.__fig.suptitle("{} Lot History Trend".format(fab))  # 总的图标题
                ax = dict()
                locater = dict()
                ax['xmc_logic'] = self.__fig.add_axes([0.05, 0.35, 0.70, 0.60])   # logic wafer history [x, y, width, length] ([0.05, 0.63, 0.70, 0.30]
                ax['xmc_dram'] = self.__fig.add_axes([0.05, 0.15, 0.70, 0.05])   # dram wafer history
                ax['xmc_3dic'] = self.__fig.add_axes([0.80, 0.15, 0.15, 0.40])   # hb wafer history
                locater['xmc_logic'] = WeekdayLocator(MONDAY)
                locater['xmc_dram'] = WeekdayLocator(MONDAY)
                locater['xmc_3dic'] = MonthLocator()

                for _layer, _wip_layer in _wip_data.items():
                    if _wip_layer.empty is True:
                        ax[_layer].set_axis_off()
                    else:
                        Mlots_id = _wip_layer['MLot_ID'].unique()     # 获取Mother Lot Id
                        lots_id = _wip_layer['Lot_ID'].unique()       # 获取Children Lot Id
                        xmin = _wip_layer['Current_Time'].min()
                        xmax = _wip_layer['Current_Time'].max()
                        ax[_layer].set_xlim(xmin, xmax)
                        ax[_layer].xaxis.set_major_locator(locater[_layer])
                        ax[_layer].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

                        # ========== 生成layer，并根据layer生成Y坐标轴 ===========
                        product_layer_list = self._layer_df[_layer].drop_duplicates(subset='layer', keep='first', inplace=False)[['layer', 'Seq']]
                        product_layer_name = product_layer_list['layer'].tolist()
                        product_layer_num = product_layer_list['Seq'].tolist()

                        for Mlot_id in Mlots_id:
                            datas = _wip_layer[(_wip_layer['MLot_ID'] == Mlot_id)]
                            for lot_id in lots_id:
                                new_data = datas[(datas['Lot_ID'] == lot_id)].copy()
                                lines = ax[_layer].plot(new_data['Current_Time'], new_data['Seq'], linestyle='-', linewidth=1, label=lot_id)
                                mplcursors.cursor(lines)  # xxxxxxxxxxx

                        ax[_layer].axes.set_yticks(product_layer_num)
                        ax[_layer].axes.set_yticklabels(product_layer_name)
                        ax[_layer].set_ylim(0, len(product_layer_name) + 1)
                        ax[_layer].yaxis.set_major_locator(MultipleLocator(1))

                        for tick in ax[_layer].get_xticklabels():
                            tick.set_rotation(90)
                            tick.set_horizontalalignment('center')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QMapDataGridHis(db='tempdb')
    main.show()
    sys.exit(app.exec_())
