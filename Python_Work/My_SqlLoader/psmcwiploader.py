#!/usr/bin/python
# -*- coding: utf-8 -*-

# 导入标准库

"""
用于更新当前Lot状态
# 1. 按Wafer Start Time/Lot Id排序;
# 2. 对于数据库不存在的Lot id,更新Lot ID. 如果数据库存在Lot id更新，则更新当前Layer, Wafer No;
# 3. 如果该Lot为分批Lot, 则在后续merge后Wafer Count为0， 故需要对当前Wafer No进行更新;
"""

import os
import datetime

# 导入第三方库
import pandas as pd
import numpy as np
import MySQLdb
import xlrd

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


# 数据库链接类定义
# ///////////////////////////////////////////////////////////////
class MySQL(object):
    def __init__(self, host='localhost', user="root", password='yp*963.', port=3306, charset='utf8'):
        """实例化后自动连接至数据库"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset

        self.confgdb = 'configdb'
        self.loaderdb = 'loader'
        self.testdb = 'testdb'

        self.testdb_config = {'user': self.user, 'password': self.password, 'host': self.host, 'database': self.testdb, 'charset': self.charset}

        self.loaderengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, self.loaderdb, self.charset)
        self.testdbengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, self.testdb, self.charset)


# 相关函数定义
# ///////////////////////////////////////////////////////////////
def RepeatWaferCheck():
    """将psmc_lot_tracing_table中的数据按MLot_ID拉出来，将前面分批的Wafer的ID从后面有的Wafer中减去"""
    mysql = MySQL()
    connection = MySQLdb.connect(**mysql.testdb_config)
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%Y/%m/%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Current_Chip_Name, Fab, Layer, Stage, 
        DATE_FORMAT(`Current_Time`,'%Y/%m/%d %H:%i:%s') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%Y/%m/%d') AS `Forecast_Date`, Qty, 
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` 
        FROM psmc_lot_tracing_table
        """)
        sql_results = cursor.fetchall()
        columnDes = cursor.description
    connection.close()

    columnNames = [columnDes[i][0] for i in range(len(columnDes))]             # 获取表头
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)     # 将从数据库中取出的元祖数据转换为dataframe
    list_mlot = list(df['MLot_ID'].drop_duplicates())                          # 提取出所有数据中唯一的MLOT_ID

    # 根据MLot_ID对数据进行遍历，并根据遍历过程中Wafer_No为1的数据，读出Wafer No
    # ///////////////////////////////////////////////////////////////
    for mlot in list_mlot:
        data = df[df.loc[:, 'MLot_ID'] == mlot].copy()  # 按lot生成data数据,包含（MLot_ID，Lot_ID，Current_Chip_Name，Current_Time，Wafer_No信息）
        if data.shape[0] > 1:
            data.sort_values(by='Current_Time', axis=0, ascending=False, inplace=True)  # 将data数据按时间排序
            # 遍历每一列，如果当列第一个为1，则后续不得为1
            for index, row in data.iteritems():
                if row.name in ['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25']:
                    # 按#01,#02 ....#25 Wafer进行重复性确认，如果重复则赋值为None
                    for i in range(len(row.values)):
                        if row.values[i] == 1:
                            row.values[i + 1:] = None
                temp = data[['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18',
                             '#19', '#20', '#21', '#22', '#23', '#24', '#25']].astype(dtype=float)
                data['Qty'] = temp.sum(axis=1, skipna=np.nan)
        else:
            pass
        # 将Wafer No数据按新的状态进行更新
        for row in data.iterrows():
            Item = row[1].where(row[1].notnull(), 'Null')  # 将nan 转变为Null
            dictdata = Item.to_dict()
            MysqlUpdate(dictdata)


def MysqlUpdate(_dictdata):
    """
    将psmc_wip_tracing_table中按Lot提取的最新信息更新至psmc_lot_tracing_table
    """
    # todo 当前需要更新整个数据库，如何提高效率？
    Lot_ID = _dictdata['Lot_ID']
    dictstr = _dictdata.copy()
    dictfloat = _dictdata.copy()
    del dictstr['Wafer_Start_Date'], dictstr['MLot_ID'], dictstr['Lot_ID'], dictstr['Qty'], dictstr['#01'], dictstr['#02'], dictstr['#03'], dictstr['#04'], dictstr['#05'], \
        dictstr['#06'], dictstr['#07'], dictstr['#08'], dictstr['#09'], dictstr['#10'], dictstr['#11'], dictstr['#12'], dictstr['#13'], dictstr['#14'], dictstr['#15'], dictstr['#16'], \
        dictstr['#17'], dictstr['#18'], dictstr['#19'], dictstr['#20'], dictstr['#21'], dictstr['#22'], dictstr['#23'], dictstr['#24'], dictstr['#25']
    del dictfloat['Wafer_Start_Date'], dictfloat['MLot_ID'], dictfloat['Lot_ID'], dictfloat['Current_Chip_Name'], dictfloat['Fab'], dictfloat['Layer'], dictfloat['Stage'], dictfloat['Current_Time'], \
        dictfloat['Forecast_Date']
    sql = "UPDATE psmc_lot_tracing_table SET {}, {} WHERE Lot_ID = '{}'".format((','.join("`{}` = '{}'".format(k, v) for k, v in dictstr.items())),
                                                                                (','.join("`{}` = {}".format(k, v) for k, v in dictfloat.items())), Lot_ID)

    mysql = MySQL()
    connection = MySQLdb.connect(**mysql.testdb_config)
    with connection.cursor() as cursor:
        try:  # 将Wafer信息更新至数据库
            cursor.execute(sql)
        except Exception as e:
            print(str(e))
        finally:
            connection.commit()
    connection.close()


def DataToWafer(_data):
    """将Wafer No 拍平 """
    serdatas = pd.Series(np.nan, index=['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                        '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'])
    if _data is not None and _data is not np.nan:
        data = _data.split(';')
        for i in data:
            serdatas['#' + i] = 1
    return serdatas


def RepeatLotCheck(_item):
    """如果需要录入的Lot_Id在psmc_lot_tracing_table数据库中已经存在，则将数据库中的该Lot信息调出，通过判断这个Lot的Current_Time确认是否需要更新"""
    mysql = MySQL()
    connection = MySQLdb.connect(**mysql.testdb_config)
    with connection.cursor() as cursor:
        cursor.execute("""USE testdb;""")
        cursor.execute("""
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%%Y/%%m/%%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Current_Chip_Name, Fab, Layer, Stage, 
        DATE_FORMAT(`Current_Time`,'%%Y/%%m/%%d %%H:%%i:%%s') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%%Y/%%m/%%d') AS `Forecast_Date`, Qty
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` 
        FROM psmc_lot_tracing_table WHERE Lot_ID = '%s'
        """ % _item['Lot_ID'].item())
        sql_results = cursor.fetchall()
        columnDes = cursor.description
    connection.close()
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)   # 将这个Lot的信息从psmc_lot_tracing_table中调出来
    # 如果数据库中的时间比excel中读取的current时间小，则更新数据，否则Pass
    ItCurrent_Time = datetime.datetime.strptime(_item['Current_Time'].item(), '%Y/%m/%d %H:%M')         # 当前需要判断的Lot的Current_Time，当前时间没有%S
    ItCurrent_Date = datetime.datetime.strptime(_item['Current_Time'].item().split(" ")[0], '%Y/%m/%d')   # current time有含有时间信息，需要转换为日期信息
    ItForecast_Date = datetime.datetime.strptime(_item['Forecast_Date'].item(), '%Y/%m/%d')     # 当前Lot的Forecast_Date
    dfCurrent_Time = datetime.datetime.strptime(df['Current_Time'].item(), '%Y/%m/%d %H:%M:%S')   # 数据库中的Current_Time
    dfCurrent_Date = datetime.datetime.strptime(df['Current_Time'].item().split(" ")[0], '%Y/%m/%d')   # current time有含有时间信息，需要转换为日期信息
    dfForecast_Date = datetime.datetime.strptime(df['Forecast_Date'].item(), '%Y/%m/%d')     # 数据库中的Forecast_Date

    if (ItCurrent_Time > dfCurrent_Time) and (dfCurrent_Date != dfForecast_Date):
        """库中的当前时间比当前Lot的时间小，说明当前Lot比库中站点更靠后；库中的时间小于库中froecast时间，说明还未到达WH; """
        _item = _item.where(_item.notnull(), 'Null')  # 将刻号没有的 #01, #02中的nan 转变为Null
        dictdata = _item.to_dict(orient='record')[0]  # 将dataframe数据转换为字典
        MysqlUpdate(dictdata)

    if (ItCurrent_Time < dfCurrent_Time) and (ItCurrent_Date == ItForecast_Date):
        """当前时间比库中时间小，且当前时间与当前Forecast_Date时间相等则说明当前Lot已经到达WH"""
        _item = _item.where(_item.notnull(), 'Null')  # 将刻号没有的 #01, #02中的nan 转变为Null
        dictdata = _item.to_dict(orient='record')[0]  # 将dataframe数据转换为字典
        MysqlUpdate(dictdata)


def DirFolder(_file_path):
    """遍历路径，返回文件的全路径"""
    _file_paths = []
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            _file_paths.append(os.path.join(root, file))

    return _file_paths


def FileRepeatChk(_file_path):
    """判断每天需要upload的文件"""
    old_name = []
    new_name = []
    mysql = MySQL()
    connection = MySQLdb.connect(**mysql.testdb_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE loader;')
            cursor.execute('SELECT filename FROM psmcwiploader')
            result = cursor.fetchall()
    finally:
        connection.close()
    for i in result:     # 将文件名元祖变成文件名列表
        for j in i:
            old_name.append(j)

    _data_paths = DirFolder(_file_path)    # 查询所有文件的路径

    for data_path in _data_paths:
        _, filename = os.path.split(data_path)
        new_name.append(filename)

    _data_paths = list(set(new_name).difference(set(old_name)))
    return _data_paths


# main
# ///////////////////////////////////////////////////////////////
def PsmcWipLoader():
    """
    主程序，主要用于将路径为file_path的Lot_ID数据上传至数据库
    """

    data_paths = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\01_PTC_Wip'

    # 确认路径中的不重复文件，并返回文件名的list
    file_paths = [data_paths + '\\' + i for i in FileRepeatChk(data_paths)]

    rename = {'Wafer Start Date': 'Wafer_Start_Date', 'MLot ID': 'MLot_ID', 'Lot ID': 'Lot_ID', 'Current Chip Name': 'Current_Chip_Name', 'Fab': 'Fab',
              'Layer': 'Layer', 'Stage': 'Stage', 'Current Time': 'Current_Time', 'Forecast Date': 'Forecast_Date', 'Qty': 'Qty', 'Wafer No': 'Wafer_No'}
    order = ['Wafer_Start_Date', 'MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'Fab', 'Layer', 'Stage', 'Current_Time', 'Forecast_Date', 'Qty', 'Wafer_No']

    # ---- 数据库设置----
    mysql = MySQL()
    # ---- 遍历文件夹中所有的文件, 并确认是否已经上传数据库，如未上传，返回路径 ----
    for file_path in file_paths:
        loadtowip = pd.DataFrame()
        try:  # 读取excel中的Current_Time(使用Try是由于有些文件打不开)
            workbook = xlrd.open_workbook(file_path, 'rb')
        except AttributeError:
            pass
        table = workbook.sheet_by_name('ALL')
        Current_Time = table.cell_value(0, 0)
        datas = pd.read_excel(file_path, sheet_name='ALL', skiprows=3, header=0)        # 读取excel中的wip信息
        datas['MLot ID'] = datas['Lot ID'].str[:6]
        # ---- 处理无Wafer No的WIP文件 ----
        try:
            datas['Wafer No']
        except KeyError:
            datas['Wafer No'] = None
        # ---- 按表的列名进行重命名，并按要求进行列排序 ----
        datas.rename(columns=rename, inplace=True)
        datas['Current_Time'] = Current_Time
        datas = datas[order]

        # ---- 上传数据至数据库 ----
        for index, row in datas.iterrows():
            wafer_no = DataToWafer(row['Wafer_No'])
            ser_total = pd.DataFrame(pd.concat([row[:-1], wafer_no])).T  # 生成单个的wip数据
            # 将Wafer信息更新psmc_lot_tracing_table, 如果为新的Lot_ID,则直接插入，如果为旧的Lot_ID，则调用RepeatLotCheck函数，
            # 但无法更新Wafer No信息，故需要RepeatWaferCheck()函数进行相应的check
            try:
                pd.io.sql.to_sql(ser_total, 'psmc_lot_tracing_table', con=mysql.testdbengine, if_exists='append', index=False)
            except Exception:
                RepeatLotCheck(ser_total)
            # 生成dataframe loadtowip用于整体录入psmc_wip_tracing_table数据库
            loadtowip = loadtowip.append(ser_total)

        # --- 更新psmc_wip_tracing_table ----
        try:
            pd.io.sql.to_sql(loadtowip, 'psmc_wip_tracing_table', con=mysql.testdbengine, if_exists='append', index=False)
        except Exception:  # 如果由于Lot ID重复导致无法更新，则调用RepeatLotCheck函数
            pass
        # ---- 将上传的文件更新至psmwiploader中 ----
        _, filename = os.path.split(file_path)
        loader_record = pd.DataFrame({'filename': filename}, index=[0])
        try:
            pd.io.sql.to_sql(loader_record, 'psmcwiploader', con=mysql.loaderengine, if_exists='append', index=False)
        except Exception:
            pass
    RepeatWaferCheck()


if __name__ == "__main__":
    PsmcWipLoader()
