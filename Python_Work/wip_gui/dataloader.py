#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pymysql
import time
from Python_Work.wip_gui.PsmcWipLoader import psmcWipLoader
from Python_Work.wip_gui.PsmcLotLoader import PsmcLotLoader


def DirFolder(_file_path):
    """遍历路径，返回文件的全路径"""
    _file_paths = []
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            _file_paths.append(os.path.join(root, file))
    return _file_paths


def FileRepeatChk(_file_path):
    """判断每天需要upload的文件"""
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
            cursor.execute('USE configdb;')
            cursor.execute('SELECT filename FROM psmcwiploader')
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


def main1():
    file_path = r'F:\08 Daily_Report\01_PTC_Wip'
    data_paths = [file_path + '\\' + i for i in FileRepeatChk(file_path)]
    try:
        PsmcLotLoader(data_paths)
    except Exception as e:
        print('PsmcLotLoader ' + e)
    try:
        psmcWipLoader(data_paths)
    except Exception as e:
        print(' psmcWipLoader ' + e)


if __name__ == "__main__":
    # while True:
    #     time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    #     if time_now == '13:30:00':
    #         print("ok")
    #         time.sleep(300)
    main1()
