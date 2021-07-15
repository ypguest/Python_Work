# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
用于将XMC提供的DailyMapping上传至数据库
# 1. load mapping file
# 2. 如果文件loading成功，则将将文件名写入xmcmappingloader中
"""

import os
import datetime

# 导入第三方库
import pandas as pd
import numpy as np
import pymysql
import csv

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


# 数据库链接类定义
# ///////////////////////////////////////////////////////////////
class MySQL(object):
    def __init__(self, host='localhost', database='testdb', user="root", password='yp*963.', port=3306, charset='utf8'):
        """实例化后自动连接至数据库"""
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.sql_config = {'user': self.user, 'password': self.password, 'host': self.host, 'database': self.database, 'charset': self.charset}
        self.testdbengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, 'testdb', self.charset)
        self.loaderengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, 'loader', self.charset)


def DirFolder(_file_path):
    """遍历路径，获取文件名"""
    _file_paths = []
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            _file_paths.append(os.path.join(root, file))
    return _file_paths


def FileRepeatChk(_file_path):
    """判断每天需要upload的文件"""
    mysql = MySQL()
    connection = pymysql.connect(**mysql.sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE loader;')
            cursor.execute('SELECT filename FROM xmcmappingloader')
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
        if filename in ['Thumbs.db']:
            continue
        else:
            new_name.append(filename)
    _data_paths = list(set(new_name).difference(set(old_name)))
    return _data_paths


def mappingloader(_file_path):

    # ---- 确认路径中的不重复文件，并返回文件名的list ----
    file_paths = [_file_path + '\\' + i for i in FileRepeatChk(_file_path)]
    # ---- 数据库设置----
    mysql = MySQL()

    rename = {'XMC LOT': 'XMC_LOT_ID', 'XMC WAFER': 'XMC_WAFER_NO', 'PTC LOT': 'PSMC_LOT_ID', 'PTC WAFER': 'PSMC_WAFER_NO', 'Bond TIME': 'BOND_TIME'}

    # ---- 遍历文件夹中所有的文件, 并上传数据库，如不能上传，则返回路径 ----
    for file_path in file_paths:
        # ---- 通过读取excel中的数据 ----
        try:
            table = pd.read_csv(file_path)
        except AttributeError:
            continue

        table['XMC LOT'] = table['XMC LOT'].str[:6]
        table['PTC LOT'] = table['PTC LOT'].str[:6]
        table['XMC WAFER'] = table['XMC WAFER'].apply(lambda x: '#' + ('0' + str(x))[-2:])
        table['PTC WAFER'] = table['PTC WAFER'].apply(lambda x: '#' + ('0' + str(x))[-2:])
        table['Bond TIME'] = table['Bond TIME'].apply(lambda x: x[:4] + "-" + x[4:6] + "-" + x[6:8])
        del table['PRODUCT ID']
        # ---- 按表的列名进行重命名，并按要求进行列排序 ----
        table.rename(columns=rename, inplace=True)

        # ---- 上传数据至数据库 ----
        try:  # 将Wafer信息更新至数据库
            pd.io.sql.to_sql(table, 'xmc_mapping_table', con=mysql.testdbengine, if_exists='append', index=False)
        except Exception as e:  # 如果由于Lot ID重复导致无法更新，则打印路径
            print(e)

        # ---- 将上传的文件更新至xmcmappingloader中 ----
        _, filename = os.path.split(file_path)
        loader_record = pd.DataFrame({'filename': filename}, index=[0])
        try:
            pd.io.sql.to_sql(loader_record, 'xmcmappingloader', con=mysql.loaderengine, if_exists='append', index=False)
        except Exception:
            pass


if __name__ == "__main__":
    path = r'\\arctis\PRODUCTION\WAT\XMC\ftp.ymtc.com\Unilot\DailyMapping'
    mappingloader(path)

