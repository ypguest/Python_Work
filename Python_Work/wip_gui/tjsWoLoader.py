#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于记录TJS的工单，并上传至数据库
"""

import os
import pandas as pd
import numpy as np
import pymysql
import re
import xlrd
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


def DataToWafer(data):
    serdatas = pd.Series(np.nan, index=['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                                        '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'])
    try:
        data = re.split(',|;', data)
    except AttributeError:
        data = data
    data = list(filter(None, data))
    for i in range(len(data)):
        data[i] = ('0' + data[i])[-2:]

    for i in data:
        serdatas['#' + i] = 1
    return serdatas


def tjsWoLoader():
    pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
    file_path = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\99_TJS_Workorder'
    items = ['FELotID', 'BE Lot ID', 'Assembly config', 'Picking sorts', 'Grade', 'Wafer qty', 'Wafer ID']
    rename = {'FELotID': 'FE_Lot_ID', 'BE Lot ID': 'BE_Lot_ID', 'Assembly config': 'Assembly_Config', 'Picking sorts': 'Picking_Sorts',
              'Grade': 'Grade', 'Wafer qty': 'Wafer_Qty', 'Wafer ID': 'Wafer_ID'}
    data_paths = dir_folder(file_path)
    for data_path in data_paths:
        datas = pd.read_excel(data_path, header=0)
        datas = datas[items]
        datas.rename(columns=rename, inplace=True)
        for index, row in datas.iterrows():
            wafer_no = DataToWafer(str(row['Wafer_ID']).replace("\n", ","))
            ser_total = pd.DataFrame(pd.concat([row[:-1], wafer_no])).T
            # noinspection PyBroadException
            try:
                pd.io.sql.to_sql(ser_total, 'tjs_wo_tracking_table', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:
                continue


if __name__ == "__main__":
    tjsWoLoader()




