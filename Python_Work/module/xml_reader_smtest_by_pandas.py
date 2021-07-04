#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import datetime
import pymysql
import shutil
import numpy as np
import pandas as pd
from pandas import DataFrame
import xml.etree.ElementTree as ET

pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', 2000)         # 显示不换行


class SqlManage:

    config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }

    def __init__(self, test_flow, test_items, test_val):
        # 调试程序输入参数
        # test_flow = 'D4R1'.lower()
        # test_items = ['MOVINV8ACC', 'BUTTERFLYACC', 'SSN', 'VICTIM']
        # test_val = ['07C8C700', '2019/10/27 22:31:57', '0.0.2RD', 'D4R1', 'SCQ32GP12H1F1C-26V A', '1D2_DIMM', '1', '031ADB6036865', '031ADB6036865,0000101000404', '031ADB6036865', '031ADB6036865']
        # 录入数据转换
        self.table_name = 'module_test_{}'.format(test_flow)  # 标明
        self.item_table = 'Key_id INT(50) NOT NULL AUTO_INCREMENT, SN_id CHAR(50) NOT NULL, Test_time CHAR(50) NULL, ' \
                          'Test_ver CHAR(50) NULL, Flow CHAR(50) NULL, PN_id CHAR(50) NULL, Silk CHAR(50) NULL, Flag INT(50) NULL, ' + ", ".join([i + ' CHAR(255) NULL' for i in test_items])
        self.Primary_key = 'Key_id, SN_ID'
        self.insert_item = 'SN_id, Test_time, Test_ver, Flow, PN_id, Silk, Flag, {}'.format(', '.join(test_items))
        self.insert_value = "'{}'".format("','".join('%s' % val for val in test_val))
        # sql命令行
        self.sql_drop_tb = 'DROP TABLE %s' % self.table_name
        self.sql_create_tb = 'CREATE TABLE IF NOT EXISTS {} ({} , PRIMARY KEY ({})) ENGINE = InnoDB;'.format(self.table_name, self.item_table, self.Primary_key)
        self.sql_insert_data = 'INSERT INTO %s (%s) VALUES (%s);' % (self.table_name, self.insert_item, self.insert_value)

    # 创建数据表
    def cretable(self):
        connection = pymysql.connect(**self.config)
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute(self.sql_create_tb)

    # 删除数据表
    def drotable(self):
        connection = pymysql.connect(**self.config)
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute(self.sql_drop_tb)

    # 插入数据
    def instable(self):
        connection = pymysql.connect(**self.config)
        with connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute(self.sql_insert_data)
            connection.commit()


def dir_folder(file_path_dir):
    file_paths = []
    for root, dirs, files in os.walk(file_path_dir):
        for file in files:
            if file == "desktop.ini":
                continue
            else:
                file_paths.append(os.path.join(root, file))
    return file_paths


def get_flow(file_path_get):
    with open(file_path_get, "r") as f:
        tree = ET.parse(f)  # 载入数据
        root = tree.getroot()  # 获取根节点
        for smtest in root.findall("TESTRUN"):
            flow = smtest.find("FLOW").text
    return flow


def get_test_item(file_path_item, test_flow):
    with open(file_path_item, "r") as f_obj:
        test_items = {}
        lines = [tmp.strip() for tmp in f_obj.readlines()]
        for line in lines:
            if line.startswith("[") or line.startswith("{"):
                test_flows = "".join(line[1:-1])
                test_items[test_flows] = []
            elif line != "":
                line = re.split("=|;", line)
                if line[1] == 'ACCMOVINV8' or line[1] == 'ACCBUTTERFLY':
                    line[1] = line[1][3:]+line[1][:3]
                test_items[test_flows].append(line[1])  #
    return test_items[test_flow]


def write_to_sql(file_path_sql, test_item_write):
    test_results = DataFrame(columns=['test_time', 'test_ver', 'flow', 'pn', 'silk', 'flag'] + test_item_write)
    with open(file_path_sql, "rt") as f:
        tree = ET.parse(f)  # 载入数据
        root = tree.getroot()  # 获取根节点
        if root.tag.upper() == "SMTEST":    # 判断文件是否为SMTEST
            for smtest in root.findall("TESTRUN"):
                test_time = smtest.get('START')  # 访问START元素属性,获得测试时间
                test_time_format = datetime.datetime.strptime(test_time, '%a %b %d %H:%M:%S %Y')
                test_time = test_time_format.strftime('%Y/%m/%d %H:%M:%S')
                test_ver = smtest.find("VERSION").text  # 获取test_version
                flow = smtest.find("FLOW").text
                for mch in smtest.findall("MCH"):
                    for controller in mch.findall("./SOCKET/CONTROLLER"):
                        for channel in controller.findall("CHANNEL"):
                            for dim in channel.findall("DIMM"):
                                pn = dim.find("ID").text
                                sn = dim.find("SN").text
                                silk = dim.find("SILK").text
                                df = DataFrame({'test_time': test_time,
                                                'test_ver': test_ver,
                                                'flow': flow,
                                                'pn': pn,
                                                'silk': silk}, index=[sn])
                                test_results = test_results.append(df)
        elif root.tag.upper() == "UMTEST":
            for umtest in root.findall("TESTRUN"):
                test_time = umtest.get('START')  # 访问START元素属性,获得测试时间
                test_time_format = datetime.datetime.strptime(test_time, '%a %b %d %H:%M:%S %Y')
                test_time = test_time_format.strftime('%Y/%m/%d %H:%M:%S')
                test_ver = umtest.find("VERSION").text  # 获取test_version
                flow = umtest.find("FLOW").text
                for mch in umtest.findall("MCH"):
                    for controller in mch.findall("CONTROLLER"):
                        for channel in controller.findall("CHANNEL"):
                            for dim in channel.findall("DIMM"):
                                try:
                                    pn = dim.find("ID").text
                                except AttributeError:
                                    pn = "99999999"
                                try:
                                    sn = dim.find("SN").text
                                except AttributeError:
                                    sn = "99999999"
                                silk = dim.find("SILK").text
                                df = DataFrame({'test_time': test_time,
                                                'test_ver': test_ver,
                                                'flow': flow,
                                                'pn': pn,
                                                'silk': silk}, index=[sn])
                                test_results = test_results.append(df)
        for entry in root.findall(".//ENTRY"):  # fail sample information collect
            for algorithm in entry.findall("ALGORITHM"):
                fail_patter = algorithm.find("ALGO_NAME").text.upper()
            try:
                dimm_sn = entry.find("DIMM_SN").text
            except AttributeError:     # 规避有些数据没有SN号
                dimm_sn = '99999999'
            rank = entry.find("RANK").text
            bs = entry.find("BS").text
            bg = entry.find("BG").text
            ras = entry.find("RAS").text
            cas = entry.find("CAS").text
            try:
                dq = '0' + entry.find("ECC_DQ").text
                dq = dq[-2:]
            except AttributeError:
                dq = '0' + entry.find("DQ").text
                dq = dq[-2:]
            fail_log = DataFrame(''.join([rank, bg, bs, ras, cas, dq]), index=[dimm_sn], columns=[fail_patter])
            if test_results.loc[dimm_sn, fail_patter] is np.nan:
                test_results.loc[dimm_sn, fail_patter] = [(fail_log.loc[dimm_sn, fail_patter])]
            elif fail_log.loc[dimm_sn, fail_patter] not in test_results.loc[dimm_sn, fail_patter]:
                try:
                    test_results.loc[dimm_sn, fail_patter].append(fail_log.loc[dimm_sn, fail_patter])
                except TypeError:
                    continue
            else:
                continue
        for induex, row in test_results.iterrows():          # 判断flag 的值
            if np.count_nonzero(row[6:] != row[6:]) == len(row[6:]):
                row['flag'] = 1
            else:
                row['flag'] = 0
        test_results.fillna(str('NULL'), inplace=True)
        for index, row in test_results.iterrows():         # 写入数据到mysql
            test_sql = [index]
            for i in row.values:
                if type(i) is list:
                    i = ",".join(i)
                test_sql.append(i)
            mysql = SqlManage(flow, test_item_write, test_sql)
            mysql.cretable()
            mysql.instable()


def main(file_path_xml):
    xml_Regex = re.compile(r'\d{8}\.XML', re.I)
    file_paths = dir_folder(file_path_xml)
    for file in file_paths:
        (filepath, tempfilename) = os.path.split(file)
        if re.match(xml_Regex, tempfilename):  # 获取包含测试结果的xml文件
            test_flow = get_flow(file)  # 获取test flow
            if test_flow == "STANDARD":   # 将test_flow为"STANDARD"的文件移走
                shutil.move(file, r"C:\Users\yinpeng\Desktop\Module_Test_Result\STANDARD")
            fileregex = os.path.join(filepath, "umtest.INI")   # 读取每个测试log的测试项目名称
            if os.path.exists(fileregex):  # 返回所有匹配的文件路径列表
                test_item_main = get_test_item(''.join(fileregex), test_flow)
            write_to_sql(file, test_item_main)


if __name__ == "__main__":
    file_path = r'C:\Users\yinpeng\Desktop\Module_Test_Result\rawdata'
    main(file_path)

