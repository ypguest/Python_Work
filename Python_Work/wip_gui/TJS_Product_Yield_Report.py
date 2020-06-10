#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于记录TJS的生产wip情况，并上传至数据库
"""

import os
import pandas as pd
import numpy as np
import pymysql
import re
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


def main():
    pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb
    regex = re.compile(r'\d*')
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
    file_path = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\02_TJS_Product_Yield_Report'
    items = ['PACKAGE', 'FELOT', 'BELOT', 'LotNo', 'GRADEID', 'STAGE', 'STEP', 'Wafer in Date', 'Forecast out Date', 'Current Qty', 'Assembly In', 'Assembly Out', 'TDBI In',
             'TDBI Out', 'FT1 In', 'FT1 Out', 'FT2 In', 'FT2 Out', 'FT-OUT In', 'FT-OUT Out', 'FT5 In', 'FT5 Out', 'MSP In', 'MSP Out', 'Packing Out', 'Shipping Out']
    rename = {'Wafer in Date': 'Wafer_In_Date', 'FELOT': 'FE_Lot_ID', 'BELOT': 'BE_Lot_ID', 'LotNo': 'TJS_Lot_ID', 'Product ID': 'Product_ID', 'PACKAGE': 'Package_Type', 'GRADEID': 'Grade_ID', 'STAGE': 'Stage',
              'STEP': 'Step', 'Current Time': 'Current_Time', 'Forecast out Date': 'Forecast_Date', 'Current Qty': 'Current_Qty', 'Assembly In': 'Assembly_In', 'Assembly Out': 'Assembly_Out',
              'TDBI In': 'TDBI_In', 'TDBI Out': 'TDBI_Out', 'FT1 In': 'FT1_In', 'FT1 Out': 'FT1_Out', 'FT2 In': 'FT2_In', 'FT2 Out': 'FT2_Out', 'FT-OUT In': 'FT-OUT_In',
              'FT-OUT Out': 'FT-OUT_Out', 'FT5 In': 'FT5_In', 'FT5 Out': 'FT5_Out', 'MSP In': 'MSP_In', 'MSP Out': 'MSP_Out', 'Packing Out': 'Packing_Out', 'Shipping Out': 'Shipping_Out'}
    data_paths = dir_folder(file_path)
    for data_path in data_paths:
        xl = pd.ExcelFile(data_path)
        sheet_names = xl.sheet_names
        for sheet_name in sheet_names:
            datas = pd.read_excel(data_path, header=0, sheet_name=sheet_name, usecols=items)
            datas['Product ID'] = sheet_name
            _, file = os.path.split(data_path)
            Current_Time = list(filter(None, regex.findall(file)))
            Current_Time = ''.join(Current_Time)
            datas['Current Time'] = Current_Time
            datas.rename(columns=rename, inplace=True)
            for index, row in datas.iterrows():
                # ser_total = pd.DataFrame(row).T
                # pd.io.sql.to_sql(ser_total, 'tjs_wip_report', con=myconnect, schema='testdb', if_exists='append', index=False)
                # noinspection PyBroadException
                try:
                    ser_total = pd.DataFrame(row[['Wafer_In_Date', 'FE_Lot_ID', 'BE_Lot_ID', 'TJS_Lot_ID', 'Product_ID']]).T
                    pd.io.sql.to_sql(ser_total, 'tjs_wip_start', con=myconnect, schema='testdb', if_exists='append', index=False)
                except Exception:
                    continue


if __name__ == "__main__":
    main()

