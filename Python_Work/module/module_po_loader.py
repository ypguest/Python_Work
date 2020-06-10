#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import os

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


# 初始化
class SqlManage:

    config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }

    def __init__(self):
        self.table_name = 'module_po'
        self.table_item = 'Key_id INT(50) NOT NULL AUTO_INCREMENT, PO_No CHAR(50) NOT NULL, UniIC_PN CHAR(50) NOT NULL, Box_No CHAR(50) NULL, Pizza_No CHAR(50) NULL,' \
                          'SN_ID  CHAR(50) NOT NULL, File_Path CHAR(100) NOT NULL'
        self.Primary_key = 'Key_id, SN_ID'
        self.sql_create_tb = 'CREATE TABLE IF NOT EXISTS {} ({} , PRIMARY KEY ({})) ENGINE = InnoDB;'.format(self.table_name, self.table_item, self.Primary_key)

    # 创建数据表
    def cretable(self):
        connection = pymysql.connect(**self.config)
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute(self.sql_create_tb)

    # 删除表
    def droptable(self):
        connection = pymysql.connect(**self.config)
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute('DROP TABLE {}'.format(self.table_name))


def dir_folder(file_path):
    file_paths = []
    for root, dirs, files in os.walk(file_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for file in files:
            if file == "desktop.ini":
                continue
            else:
                file_paths.append(os.path.join(root, file))

    return file_paths


def main():
    pymysql.install_as_MySQLdb()  # 使python3.0 运行MySQLdb
    myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
    key_words = {'PO_No': ['PO'], 'Sub_PN': ['ADATA PN', '料號'], 'UniIC_PN': ['UniIC PN', '成品料号', '客户料号', '外部料号', '紫光PN', '紫光料号'],
                 'Box_No': ['箱號'], 'Pizza_No': ['pizza盒号'], 'SN_ID': ['SN号']}
    file_path = r'F:\99_DIMM_SN'

    data_paths = dir_folder(file_path)  # 生成文件名list
    for data_path in data_paths:
        # try:
        xl = pd.ExcelFile(data_path)  # 获取excel对象
        for i in range(len(xl.sheet_names)):
            df = pd.read_excel(data_path, sheet_names=i)  # 按sheet直接读取excel的数据，并获得dataframe
            df['File_Path'] = data_path  # 增加文件路径列
            for key, value in key_words.items():  # 将columns的名称改为key_word中的key值
                c = [x for x in key_words[key] if x in df.columns]
                df.rename(columns={''.join(c): key}, inplace=True)
            df.dropna(axis='index', how='any', inplace=True)   # print(df[df.isnull().T.any()])
            pd.io.sql.to_sql(df.loc[:, ['PO_No', 'UniIC_PN', 'Box_No', 'Pizza_No', 'SN_ID', 'File_Path']], 'module_po', con=myconnect, schema='testdb', if_exists='append', index=False)
        # except xlrd.XLRDError:
        #     print(data_path)


if __name__ == "__main__":

    # 创建新表
    # mysql = SqlManage()
    # mysql.droptable()
    # mysql.cretable()

    # 写入数据库
    main()


