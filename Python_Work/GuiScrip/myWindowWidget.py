# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_MainWindow import Ui_MainWindow
from mysqlconfig import MySQL

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.MainWindow = Ui_MainWindow()
        self.MainWindow.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon(r'../GuiPackage/images/ico/UniIC_Logo.ico'))

        # =================== 参数定义 =======================
        self.fab = 'PSMC'
        self.prodFam = ''
        self.proName = ''
        self.proVer = ''

        # ================== 数据录入 =======================
        # ========== Product Family QListView设置 ==========
        self.listModelFam = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewFam = ProdFamList("Nick_Name")     # 创建数据源, 查询Product_Version中Nick_Name的列表
        self.listModelFam.setStringList(self.listViewFam)       # 将数据和模型进行关联
        self.MainWindow.box1View.setModel(self.listModelFam)             # 模型与空间关联

        # ========== Product ID QListView设置 ===========
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewPid = ProdList("UniIC_Product_ID", self.fab)  # 通过数据库查询Product_ID, 并根据结果创建数据源
        self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
        self.MainWindow.box2prodList.setModel(self.listModelPid)             # 模型与控件关联
        # 属性设置
        self.MainWindow.box2prodList.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.MainWindow.box2prodList.clicked.connect(self.clickedPid)

        # ========== Product Version QListView设置 ==========
        self.listModeVer = QStringListModel()           # 创建封装列表数据源的模型
        self.listViewVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源
        self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联
        self.MainWindow.box2VerList.setModel(self.listModeVer)             # 模型与空间关联
        # 属性设置
        self.MainWindow.box2VerList.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 支持多选
        self.MainWindow.box2VerList.clicked.connect(self.clickedVer)

    # ========== 由connectSlotsByName() 自动连接的槽函数==================
    def on_box1View_clicked(self, selectedIndexe):
        """若box1View内容被选中则将box1View选择的结果反馈到box1LineEdit中"""
        self.MainWindow.box1LineEdit.setText(self.listViewFam[selectedIndexe.row()])

    def on_box1LineEdit_textChanged(self):
        """若box1LineEdit的内容发生改变，则将该内容传递给 @self.prodFam"""
        self.prodFam = self.MainWindow.box1LineEdit.text()

        # 根据@self.prodFam的内容更新self.listViewPid，self.listViewVer
        if len(self.prodFam) == 0:
            # ==== 如果ProdFam的数据为空，则根据Fab进行查询 ====
            self.listViewPid = ProdList("UniIC_Product_ID", self.fab)     # 通过数据库查询Product_ID, 并根据结果创建数据源
            self.listModelPid.setStringList(self.listViewPid)       # 将模型中的数据进行更新
            self.listViewVer = ProdList("UniIC_Product_Version", self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将模型中的数据进行更新
        else:
            # ---- 如果ProdFam有数据，则根据ProdFam和Fab信息进行查询 ----
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联
        # 将box2LineEdit重置
        self.MainWindow.box2LineEdit.setText("")

    def on_box2Button1_toggled(self, bools):
        if bools:
            self.fab = 'PSMC'
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联

    def on_box2Button2_toggled(self, bools):
        if bools:
            self.fab = 'XMC'
            self.listViewPid = InputQueryId(self.prodFam, self.fab)
            self.listModelPid.setStringList(self.listViewPid)       # 将数据和模型进行关联
            self.listViewVer = InputQueryVer(self.prodFam, self.fab)     # 创建数据源
            self.listModeVer.setStringList(self.listViewVer)       # 将数据和模型进行关联

    def on_box3fcnbtn1_pressed(self):
        productinfo = dict()
        productinfo['Nick_Name'] = [self.prodFam]
        productinfo['Fab'] = [self.fab]
        productinfo['UniIC_Product_ID'], productinfo['UniIC_Product_Version'] = prodIdCov(self.MainWindow.box2LineEdit.text())
        columns = list(productinfo.keys())  # 获取参数名['Nick_Name','Fab','UniIC_Product_ID','UniIC_Product_Version']
        for key in columns:  # 如果参数为空，则去掉该参数
            if productinfo[key] == ['']:
                del productinfo[key]
        productid = getProductId(productinfo)  # 输入产品信息，生成PowerChip_Product_Version List字典
        lot_df = DailyWipCheck(productid, productinfo['Fab'])



        #
        # if self.MainWindow.box2LineEdit.text() == '':
        #     pass
        # else:
        #
        #     self.lot_df = DailyWipCheck(productid, productinfo['Fab'])
        #     self.TableWidget.writeData(self.lot_df)   # 将查询的结果写入sqlite数据库(tempdb)
        #     self.TableWidget.setTableView()


    # ========== 由自定义函数连接的槽函数==================
    def clickedPid(self):
        """当数据进行切换时，将选中的Product ID数据放入LineEdit中"""
        datalist = list()
        for i in self.MainWindow.box2prodList.selectedIndexes():
            datalist.append(i.data())
        self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist) + ']')      # 将LineEdit里的内容进行写入lineEdit
        self.listViewVer = ProdQueryVerList(datalist, self.fab)     # 创建数据源
        self.listModeVer.setStringList(self.listViewVer)  # 将数据和模型进行关联

    def clickedVer(self):
        """定义单击List中的Ver事件，如果当lineEdit.text()为空时，则将版本放入"""
        datalist = list()
        # ---- 将点击的内容变成list ----
        for i in self.MainWindow.box2VerList.selectedIndexes():
            datalist.append(i.data())
        if self.MainWindow.box2LineEdit.text() == '' or re.findall(r'\[V\d*\]', self.MainWindow.box2LineEdit.text()):
            self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist) + ']')  # 将LineEdit里的内容进行写入lineEdit
        else:
            matchobj = re.split(r'\[|\],\[|\]', self.MainWindow.box2LineEdit.text())
            matchobj = [i for i in matchobj if i != '']
            for i in range(len(matchobj)):
                if matchobj[i].split(','):
                    matchobj[i] = matchobj[i].split(',')[0]
            datalist1 = []
            for i in range(len(matchobj)):
                for j in range(len(datalist)):
                    datalist1.append(matchobj[i] + ',' + datalist[j])
            self.MainWindow.box2LineEdit.setText('[' + '],['.join(datalist1) + ']')


def prodIdCov(value):
    productId = list()
    productVer = list()
    prodVerreg1 = re.compile(r'\[[A-Za-z0-9_.*+%!()\-]*,V\d*\]')
    prodVerreg2 = re.compile(r'\[V\d*\]')
    if value is None:
        pass
    elif re.findall(prodVerreg1, value):
        for i in re.findall(prodVerreg1, value):
            productId.append(i.strip('[|]').split(',')[0])
            productVer.append(i.strip('[|]').split(',')[1])
        productId = list(set(productId))
        productVer = list(set(productVer))
    elif re.findall(prodVerreg2, value):
        for i in re.findall(prodVerreg2, value):
            productVer.append(i.strip('[|]'))
        productId = ['']
    else:
        for i in value.split('],['):
            productId.append(i.strip('[|]'))
        productVer = ['']
    return productId, productVer


def getProductId(productinfo):
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


def DailyWipCheck(productid, Fab):
    """通过查询当前数据库中最新的时间，根据时间反差当前Lot的信息"""
    # ---- 变量定义----
    set_time = dict()
    set_time['Fab'] = Fab
    tbname = '{}_lot_tracing_table'.format(set_time['Fab'][0].lower())
    # ---- 连接数据库 ----
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    time_des, time_sql_res = mysql.fetchAll(tbname=tbname, items=['Current_Time'])
    time_df = pd.DataFrame(time_sql_res, columns=time_des)  # 生成current_time的dataframe
    time_df.sort_values(by='Current_Time', ascending=False, inplace=True)
    set_time['Current_Time'] = [time_df.iat[0, 0].date()]  # iat基于索引位置的选择方法, 找出最近的时间
    set_time['Current_Chip_Name'] = productid['{}_Product_ID'.format(set_time['Fab'][0])]  # 将Current_Chip_Name加入setting time字典，用于sql的筛选条件

    # ---- 连接数据库查询 ----
    mysql.selectDb('testdb')  # 连接数据库
    _sql = "a.Current_Chip_Name = '" + "' OR a.Current_Chip_Name= '".join(set_time['Current_Chip_Name']) + "'"
    sqlquery = """Select a.index, a.Wafer_Start_Date, a.MLot_ID, a.Lot_ID, b.UniIC_Product_ID, b.UniIC_Product_Version, a.Fab, a.Stage, DATE_FORMAT(a.Current_Time, '%Y-%m-%d') AS 'Current_Time',
        a.Forecast_Date, a.Qty, a.`#01`, a.`#02`, a.`#03`, a.`#04`, a.`#05`, a.`#06`, a.`#07`, a.`#08`, a.`#09`, a.`#10`, a.`#11`, a.`#12`, a.`#13`, a.`#14`, a.`#15`, a.`#16`, a.`#17`, a.`#18`,
        a.`#19`, a.`#20`, a.`#21`, a.`#22`, a.`#23`, a.`#24`, a.`#25` FROM testdb.`{0}_lot_tracing_table` AS a JOIN configdb.`{0}_product_version` AS b on
        a.Current_Chip_Name = b.{1}_Product_ID WHERE ({2}) and (DATE_FORMAT(a.Current_Time, '%Y-%m-%d') = '{3}')""".format(
        set_time['Fab'][0].lower(), set_time['Fab'][0], _sql, set_time['Current_Time'][0])
    lotche_des, lotche_sql_res = mysql.sqlAll(sqlquery)
    mysql.cur.close()
    lot_df = pd.DataFrame(lotche_sql_res, columns=lotche_des)
    lot_df.set_index(["index"], inplace=True)  # 将dataframe中'index'设置为index

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


def ProdFamList(query1):
    """用于FamilyQuery & ProdQuery中, 输入Item(Product_ID or Ver)，并查找psmc_product_version表中所有的匹配值(List)"""
    # ---- 查询pmsc的nick_name
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM psmc_product_version ORDER By '%s'" % (query1, query1)
    desc1, result1 = mysql.sqlAll(sql)
    res1 = [result1[i][0] for i in range(len(result1))]

    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM xmc_product_version ORDER By '%s'" % (query1, query1)
    desc2, result2 = mysql.sqlAll(sql)
    res2 = [result2[i][0] for i in range(len(result2))]
    result = res1 + res2
    result = sorted(list(set(result))[:])
    return result


def ProdList(query1, fab):
    """用于FamilyQuery & ProdQuery中, 输入Item(Product_ID or Ver)，并查找psmc_product_version表中所有的匹配值(List)"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT %s FROM %s_product_version ORDER By '%s'" % (query1, fab, query1)
    desc, result = mysql.sqlAll(sql)
    return sorted([result[i][0] for i in range(len(result))])


def ProdQueryVerList(items, fab):
    """用于ProdQuery中, 实现输入UniIC_Product_Id（1G-H45），查找出对应的所有UniIC_Product_Version(V05)"""

    results = list()
    mysql = MySQL()
    mysql.selectDb('configdb')
    for item in items:
        sql = "SELECT DISTINCT UniIC_Product_Version FROM %s_product_version WHERE UniIC_Product_Id = '%s' ORDER By UniIC_Product_Version" % (fab, item)
        desc, result = mysql.sqlAll(sql)
        results.extend([result[i][0] for i in range(len(result))])
    results = list(set(results))[:]
    for i in range(len(results)-1):
        if int(results[i].replace('V', '')) > int(results[i+1].replace('V', '')):
            for j in range(i+1, 0, -1):
                if int(results[j].replace('V', '')) < int(results[j-1].replace('V', '')):
                    results[j-1], results[j] = results[j], results[j-1]
                else:
                    break
    return sorted(results)


def InputQueryId(query, fab):
    """用于ProdQuery中, 实现输入Nick_Name，查找出对应的所有UniIC_Product_ID"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT UniIC_Product_ID FROM %s_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_ID" % (fab, query)
    desc, result = mysql.sqlAll(sql)
    return [result[i][0] for i in range(len(result))]


def InputQueryVer(query, fab):
    """用于ProdQuery中, 输入Nick_Name，查找出对应的所有UniIC_Product_Version"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT UniIC_Product_Version FROM %s_product_version WHERE Nick_Name = '%s' ORDER By UniIC_Product_Version" % (fab, query)
    desc, result = mysql.sqlAll(sql)
    return [result[i][0] for i in range(len(result))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindows()
    main.show()
    sys.exit(app.exec_())