#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于更新数据库中psmc_wip_tracing_table，同时将已经更新的文件路径记录到psmc_loader文件中
在所有脚本中的顺序
01 PsmcWipLoader
02 TjsTestYieldLoader
03 TjsWoLoader

"""

import os
import pandas as pd
import numpy as np
import pymysql
import xlrd
from sqlalchemy import create_engine


def DirFolder(file_path):
    """遍历路径，返回文件的全路径"""
    file_paths = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def DataToWafer(data):
    """将Data: #01,#02,#03....数据转换为 独立的#01:1, #02:1, #03:1"""
    serdatas = pd.Series(np.nan, index=['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                        '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'])
    if data is not None and data is not np.nan:
        data = data.split(';')
        for i in data:
            serdatas['#' + i] = 1
    return serdatas


def FileRepeatChk(_file_path):
    # todo 判断每天需要upload的文件
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'configdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute('SELECT filename FROM wiploader')
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


def psmcWipLoader(data_paths):
    """输入需要上传的数据路径列表"""
    pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
    rename = {'Wafer Start Date': 'Wafer_Start_Date', 'MLot ID': 'MLot_ID', 'Lot ID': 'Lot_ID', 'Current Chip Name': 'Current_Chip_Name', 'Fab': 'Fab',
              'Layer': 'Layer', 'Stage': 'Stage', 'Current Time': 'Current_Time', 'Forecast Date': 'Forecast_Date', 'Qty': 'Qty', 'Wafer No': 'Wafer_No'}
    order = ['Wafer_Start_Date', 'MLot_ID', 'Lot_ID', 'Current_Chip_Name', 'Fab', 'Layer', 'Stage', 'Current_Time', 'Forecast_Date', 'Qty', 'Wafer_No']
    for data_path in data_paths:    # 遍历文件夹中所有的文件, 并确认是否已经上传数据库，如未上传，返回路径
        print("#02", data_path)
        try:         # 通过读取excel获取Current_Time， 有些文件打不开
            workbook = xlrd.open_workbook(data_path, 'rb')
        except AttributeError:
            continue
        table = workbook.sheet_by_name('ALL')
        Current_Time = table.cell_value(0, 0)
        datas = pd.read_excel(data_path, sheet_name='ALL', skiprows=3, header=0)    # 读取excel中的wip信息
        datas['MLot ID'] = datas['Lot ID'].str[:6]
        # todo 处理无Wafer No的WIP文件
        try:
            datas['Wafer No']
        except KeyError:
            datas['Wafer No'] = None
        # todo 按表的列名进行重命名，并按要求进行列排序
        datas.rename(columns=rename, inplace=True)
        datas['Current_Time'] = Current_Time
        datas = datas[order]
        # todo 将上传的文件名进行记录，用于建立上传数据的数据库
        _, filename = os.path.split(data_path)
        loader_record = pd.DataFrame({'filename': filename}, index=[0])
        # noinspection PyBroadException
        try:
            pd.io.sql.to_sql(loader_record, 'wiploader', con=myconnect, schema='configdb', if_exists='append', index=False)
        except Exception:
            continue
        # todo 上传wip数据
        for index, row in datas.iterrows():
            wafer_no = DataToWafer(row['Wafer_No'])
            ser_total = pd.DataFrame(pd.concat([row[:-1], wafer_no])).T
            # noinspection PyBroadException
            try:
                pd.io.sql.to_sql(ser_total, 'psmc_wip_tracing_table', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:
                continue


if __name__ == "__main__":
    psmcWipLoader()
