#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
用于更新当前Lot状态
1. 按Wafer Start Time/Lot Id排序;
2. 对于数据库不存在的Lot id,更新Lot ID. 如果数据库存在Lot id更新，则更新当前Layer, Wafer No;
3. 如果该Lot为分批Lot, 则在后续merge后Wafer Count为0， 故需要对当前Wafer No进行更新;
"""

import os
import datetime
import pandas as pd
import numpy as np
import pymysql
import xlrd
from sqlalchemy import create_engine
# ---------------------------pd设置-----------------------------------
# --------------------------------------------------------------------
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行
pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb


# ---------------------------------主程序1----------------------------------
def xmcWipLoader(_data_paths):
    """遍历excel数据(路径为data_paths.list())，将Lot_ID不同的产品上传至数据库, 生成xmc的wip tracing table """
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/configdb?charset=utf8')
    rename = {'Start Date': 'Wafer_Start_Date', 'MLot ID': 'MLot_ID', 'Lot ID': 'Lot_ID', 'Product ID': 'Current_Chip_Name', 'Fab': 'Fab',
              'Layer': 'Layer', 'Stage': 'Stage', 'Current Time': 'Current_Time', 'Sche. Date': 'Forecast_Date', 'QTY': 'Qty', 'WAFER_ID': 'Wafer_No'}
    order = ['Wafer_Start_Date', 'MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'Fab', 'Layer', 'Stage', 'Current_Time', 'Forecast_Date', 'Qty', 'Wafer_No']
    # ------------遍历文件夹中所有的文件, 并确认是否已经上传数据库，如未上传，返回路径-----------------
    for data_path in _data_paths:
        # --------通过读取excel获取Current_Time(使用Try是有些文件打不开)-----------------------------------
        try:
            datas = pd.read_csv(data_path)
        except AttributeError:
            continue
        # -------------------按表的列名进行重命名，并按要求进行列排序----------------
        time = os.path.split(data_path)[-1].split('_')[-1].split('.')[0]
        datas['MLot ID'] = datas['Lot ID'].str[:6]
        datas['Fab'] = 'P10'
        datas['Layer'] = datas.Stage.apply(lambda x: x.split('-')[0])
        datas['Current Time'] = time[0:4] + '/' + time[4:6] + '/' + time[6:8] + ' ' + time[8:10] + ':' + time[10:12] + ':' + time[12:14]
        datas.rename(columns=rename, inplace=True)
        datas = datas[order]
        # ------------------上传数据至------------------------------------------
        for index, row in datas.iterrows():
            wafer_no = DataToWafer(row['Wafer_No'])
            ser_total = pd.DataFrame(pd.concat([row[:-1], wafer_no])).T
            # noinspection PyBroadException
            try:     # 将Wafer信息更新至数据库
                pd.io.sql.to_sql(ser_total, 'xmc_wip_tracing_table', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:      # 如果由于Lot ID重复导致无法更新，则调用RepeatLotCheck函数
                pass


# ---------------------------------主程序2----------------------------------
def xmcLotLoader(_data_paths):
    """生成xmc lot的信息"""
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/configdb?charset=utf8')
    rename = {'Start Date': 'Wafer_Start_Date', 'MLot ID': 'MLot_ID', 'Lot ID': 'Lot_ID', 'Product ID': 'Current_Chip_Name', 'Fab': 'Fab',
              'Layer': 'Layer', 'Stage': 'Stage', 'Current Time': 'Current_Time', 'Sche. Date': 'Forecast_Date', 'QTY': 'Qty', 'WAFER_ID': 'Wafer_No'}
    order = ['Wafer_Start_Date', 'MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'Fab', 'Layer', 'Stage', 'Current_Time', 'Forecast_Date', 'Qty', 'Wafer_No']
    # ------------遍历文件夹中所有的文件, 并确认是否已经上传数据库，如未上传，返回路径-----------------
    for data_path in _data_paths:
        # --------通过读取excel获取Current_Time(使用Try是有些文件打不开)-----------------------------------
        try:
            datas = pd.read_csv(data_path)
        except AttributeError:
            continue
        # -------------------按表的列名进行重命名，并按要求进行列排序----------------
        time = os.path.split(data_path)[-1].split('_')[-1].split('.')[0]
        datas['MLot ID'] = datas['Lot ID'].str[:6]
        datas['Fab'] = 'P10'
        datas['Layer'] = datas.Stage.apply(lambda x: x.split('-')[0])
        datas['Current Time'] = time[0:4] + '/' + time[4:6] + '/' + time[6:8] + ' ' + time[8:10] + ':' + time[10:12] + ':' + time[12:14]
        datas.rename(columns=rename, inplace=True)
        datas = datas[order]

        # ------------------上传数据至------------------------------------------
        for index, row in datas.iterrows():
            wafer_no = DataToWafer(row['Wafer_No'])
            ser_total = pd.DataFrame(pd.concat([row[:-1], wafer_no])).T
            # noinspection PyBroadException
            try:     # 将Wafer信息更新至数据库
                pd.io.sql.to_sql(ser_total, 'xmc_lot_tracing_table', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:  # 如果由于Lot ID重复导致无法更新，则调用RepeatLotCheck函数
                RepeatLotCheck(ser_total)
    RepeatWaferCheck()


def RepeatWaferCheck():
    """将MLot按子批拉出来，将Current_Time小的Lot的分批Wafer的ID从后面有的Wafer中减去"""
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute("""
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%Y/%m/%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Current_Chip_Name, Fab, Layer, Stage,
        DATE_FORMAT(`Current_Time`,'%Y/%m/%d %H:%i:%s') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%Y/%m/%d') AS `Forecast_Date`, Qty,
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25`
        FROM xmc_lot_tracing_table
        """)
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]             # 获取表头
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)     # 将从数据库中取出的元祖数据转换为dataframe
    df.drop_duplicates(subset=['Lot_ID'], keep='first', inplace=True)          # 将dataframe中Lot_id相同的数据，只保留第一次的
    list_mlot = list(df['MLot_ID'].drop_duplicates())                          # 提取出所有数据中唯一的MLOT_ID
    # ----------根据Mother lot id对数据进行遍历，并根据遍历过程中Wafer No为1的数据，读出Wafer No, 并将Lot Wafer信息进行写入psmc_lot_wafer数据库中------
    for mlot in list_mlot:
        data = df[df.loc[:, 'MLot_ID'] == mlot].copy()  # 按lot生成data数据,包含（MLot_ID，Lot_ID，Current_Chip_Name，Current_Time，Wafer信息）
        if data.shape[0] > 1:
            data.sort_values(by='Current_Time', axis=0, ascending=False, inplace=True, na_position='first')
            # ---遍历每一列，如果当列第一个为1，则后续不得为1
            for index, row in data.iteritems():
                if row.name in ['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25']:
                    # 按#01,#02 ....#25 Wafer进行重复性确认，如果重复赋值为None

                    for i in range(len(row.values)):
                        if row.values[i] == 1:
                            row.values[i + 1:] = None
                temp = data[['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18',
                             '#19', '#20', '#21', '#22', '#23', '#24', '#25']].astype(dtype=float)
                data['Qty'] = temp.sum(axis=1, skipna=np.nan)
        else:
            pass
        for row in data.iterrows():
            Item = row[1].where(row[1].notnull(), 'Null')  # 将nan 转变为Null
            dictdata = Item.to_dict()
            MysqlUpdate(dictdata)


def RepeatLotCheck(Item):
    """如果录入的Lot_Id.dataframe()与数据库中已经存在的Lot_Id，则将数据库中的该Lot信息调出，通过判断这个Lot的Current_Time确认是否需要更新"""
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute("""
        SELECT DATE_FORMAT(`Wafer_Start_Date`,'%%Y/%%m/%%d') AS `Wafer_Start_Date`, MLot_ID, Lot_ID, Current_Chip_Name, Fab, Layer, Stage, 
        DATE_FORMAT(`Current_Time`,'%%Y/%%m/%%d %%H:%%i:%%s') AS `Current_Time`, DATE_FORMAT(`Forecast_Date`, '%%Y/%%m/%%d') AS `Forecast_Date`, Qty
        `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` 
        FROM xmc_lot_tracing_table WHERE Lot_ID = '%s'
        """ % Item['Lot_ID'].item())
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)  # 将这个Lot的信息从psmc_lot_tracing_table中调出来
    # 如果数据库中的时间比excel中读取的current时间小，则更新数据，否则Pass
    ItCurrent_Time = datetime.datetime.strptime(Item['Current_Time'].item(), '%Y/%m/%d %H:%M:%S')  # 当前需要判断的Lot的Current_Time
    dfCurrent_Time = datetime.datetime.strptime(df['Current_Time'].item(), '%Y/%m/%d %H:%M:%S')  # 数据库中的Current_Time

    if ItCurrent_Time > dfCurrent_Time:
        """库中的时间比需要更新的时间小，说明当前站点比库中站点靠后，并且库中站点与当前站点不一致，则需要更新库"""
        Item = Item.where(Item.notnull(), 'Null')  # 将刻号没有的 #01, #02中的nan 转变为Null
        dictdata = Item.to_dict(orient='record')[0]  # 将dataframe数据转换为字典
        MysqlUpdate(dictdata)


def MysqlUpdate(dictdata):
    """更新数据库中Lot的最新信息"""
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    Lot_ID = dictdata['Lot_ID']
    dictstr = dictdata.copy()
    dictfloat = dictdata.copy()
    del dictstr['Wafer_Start_Date'], dictstr['MLot_ID'], dictstr['Lot_ID'], dictstr['Qty'], dictstr['#01'], dictstr['#02'], dictstr['#03'], dictstr['#04'], dictstr['#05'], \
        dictstr['#06'], dictstr['#07'], dictstr['#08'], dictstr['#09'], dictstr['#10'], dictstr['#11'], dictstr['#12'], dictstr['#13'], dictstr['#14'], dictstr['#15'], dictstr['#16'], \
        dictstr['#17'], dictstr['#18'], dictstr['#19'], dictstr['#20'], dictstr['#21'], dictstr['#22'], dictstr['#23'], dictstr['#24'], dictstr['#25']
    del dictfloat['Wafer_Start_Date'], dictfloat['MLot_ID'], dictfloat['Lot_ID'], dictfloat['Current_Chip_Name'], dictfloat['Fab'], dictfloat['Layer'], dictfloat['Stage'], dictfloat['Current_Time'], \
        dictfloat['Forecast_Date']
    sql = "UPDATE xmc_lot_tracing_table SET {}, {} WHERE Lot_ID = '{}'".format((','.join("`{}` = '{}'".format(k, v) for k, v in dictstr.items())),
                                                                                (','.join("`{}` = {}".format(k, v) for k, v in dictfloat.items())), Lot_ID)
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        try:  # 将Wafer信息更新至数据库
            cursor.execute(sql)
        except Exception:  # 如果由于Lot ID重复导致无法更新，则调用RepeatLotCheck函数
            print(sql)
        connection.commit()
        cursor.close()
        connection.close()


def DataToWafer(data):
    """将Wafer_No拍平"""
    serdatas = pd.Series(np.nan, index=['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                        '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'])
    if data is not None and data is not np.nan:
        data = data.split('.')
        for i in data:
            serdatas['#' + i] = 1
    return serdatas


def FileRepeatChk(_file_path):
    """判断每天需要upload的文件"""
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE configdb;')
            cursor.execute('SELECT filename FROM xmcwiploader')
            result = cursor.fetchall()
    finally:
        connection.close()
    old_name = []
    new_name = []
    for i in result:     # 将文件名元祖变成文件名列表
        for j in i:
            old_name.append(j)
    _data_paths = DirFolder(_file_path)    # 查询所有文件的路径
    for data_path in _data_paths:
        _, filename = os.path.split(data_path)
        new_name.append(filename)
    _data_paths = list(set(new_name).difference(set(old_name)))
    return _data_paths


def DirFolder(_file_path):
    """遍历路径，获取文件名"""
    _file_paths = []
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            _file_paths.append(os.path.join(root, file))
    return _file_paths


if __name__ == "__main__":
    file_path = r'Z:\QRE\04_QA(Component)\99_Daily_Report\19_XMC_WIP Report'
    # file_path = [r'Z:\QRE\04_QA(Component)\99_Daily_Report\19_XMC_WIP Report\XMC_wip_20200323105700349.csv']
    data_paths = [file_path + '\\' + i for i in FileRepeatChk(file_path)]
    xmcLotLoader(data_paths)


