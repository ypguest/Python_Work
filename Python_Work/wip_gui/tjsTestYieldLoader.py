#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于记录TJS的生产wip情况，并上传至数据库
"""

import os
import re
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine


# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


def dir_folder(file_path):
    file_paths = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def file_repeat_chk(file_path):
    # todo 判断每天需要upload的文件
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE configdb;')
            cursor.execute('SELECT filename FROM testloader')
            result = cursor.fetchall()
    finally:
        connection.close()
    old_name = []
    new_name = []
    for i in result:     # 将文件名元祖变成文件名列表
        for j in i:
            old_name.append(j)
    data_paths = dir_folder(file_path)    # 查询所有文件的路径
    for data_path in data_paths:
        _, filename = os.path.split(data_path)
        new_name.append(filename)
    data_paths = list(set(new_name).difference(set(old_name)))
    return data_paths


def tjsTestYieldLoader():
    pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
    file_path = r'Z:\QRE\04_QA(Component)\99_Daily_Report\03_TJS_Testing_Yield_Report'
    rename = {'LOT NO': 'LOT_NO', 'C LOT NO': 'C_LOT_NO', 'TEMP/Time': 'Test_Time', 'INPUT QTY': 'INPUT_QTY', 'PASS QTY': 'PASS_QTY'}
    items_bi = ['Product', 'LOT_NO', 'C_LOT_NO', 'STAGE', 'Test_Time', 'Weekly', 'Monthly', 'STATION', 'STATUS', 'INPUT_QTY', 'PASS_QTY', 'YIELD', 'BIN1', 'BIN2', 'BIN3', 'BIN4', 'BIN5', 'BIN6', 'BIN7',
                'BIN8', 'BIN9', 'BIN10', 'BIN11', 'BIN12', 'BIN13', 'BIN14', 'BIN15', 'BIN16', 'BIN17', 'BIN18', 'BIN19', 'BIN20', 'BIN21', 'BIN22', 'BIN23', 'BIN24', 'BIN25', 'BIN26', 'BIN27', 'BIN28',
                'BIN29', 'BIN30', 'BIN31', 'BIN32', 'Damage', 'LOSS', 'Tester', 'Device', 'P/N']
    items_ft = ['Product', 'LOT_NO', 'C_LOT_NO', 'STAGE', 'Version', 'Tester', 'Test_Time', 'Weekly', 'Monthly', 'STATION', 'STATUS', 'INPUT_QTY', 'PASS_QTY', 'YIELD', 'BIN1', 'BIN2', 'BIN3', 'BIN4', 'BIN5', 'BIN6',
                'BIN7', 'BIN8', 'Damage', 'LOSS', 'Tester', 'Device', 'P/N']

    # Todo 遍历文件夹中所有的文件, 并确认是否已经上传数据库，如未上传，返回路径
    data_paths = [file_path + '\\' + i for i in file_repeat_chk(file_path)]

    for data_path in data_paths:
        # todo 将bi及ft测试数据上传至tjs_bi_testing_yield_report & tjs_ft_testing_yield_report数据库
        datas_bi = pd.read_excel(data_path, sheet_name='BI', header=0)
        datas_bi.rename(columns=rename, inplace=True)
        datas_ft = pd.read_excel(data_path, sheet_name='FT', header=0)
        datas_ft.rename(columns=rename, inplace=True)

        # noinspection PyBroadException
        pd.io.sql.to_sql(datas_bi[items_bi], 'tjs_bi_testing_yield_report', con=myconnect, schema='testdb', if_exists='append', index=False)
        pd.io.sql.to_sql(datas_ft[items_ft], 'tjs_ft_testing_yield_report', con=myconnect, schema='testdb', if_exists='append', index=False)

        # todo 将上传的文件名进行记录，用于建立上传数据的数据库
        _, filename = os.path.split(data_path)
        loader_record = pd.DataFrame({'filename': filename}, index=[0])
        # noinspection PyBroadException
        try:
            pd.io.sql.to_sql(loader_record, 'testloader', con=myconnect, schema='configdb', if_exists='append', index=False)
        except Exception:
            continue


if __name__ == "__main__":
    main()
