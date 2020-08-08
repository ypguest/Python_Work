#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于生成psmc_lot_wafer, 并根据tjs_wo_tracking_table将tjs的Lot id与pscm Wafer进行连接
"""

import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine


class MySQL(object):
    def __init__(self, host='localhost', database='testdb', user="root", password='yp*963.', port=3306, charset='utf8'):
        """实例化后自动连接至数据库"""
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.sql_config = {'user': '{}', 'password': '{}', 'host': '{}', 'database': '{}', 'charset': '{}'.format(self.user, self.password, self.host, self.database, self.charset)}


def GenLotWafer():
    # todo 从psmc_wip_traceing_table数据中获取当前时间=出货时间的lot信息，并返回元祖
    mysql = MySQL(database='testdb', password='yp*963.')
    connection = pymysql.connect(**mysql.sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute("""SELECT MLot_ID, Lot_ID, `Current_Chip_Name`,`Current_Time`, Qty, `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, 
        `#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` FROM psmc_wip_traceing_table WHERE TO_DAYS(`Current_Time`) = TO_DAYS(`Forecast_Date`) ORDER BY `Current_time` ASC;
        """)
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]             # 获取表头
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)     # 将从数据库中取出的元祖数据转换为dataframe
    df.drop_duplicates(subset=['Lot_ID'], keep='first', inplace=True)          # 将dataframe中Lot_id相同的数据，只保留第一次的
    list_mlot = list(df['MLot_ID'].drop_duplicates())                          # 提取出所有数据中唯一的MLOT_ID

    # todo 根据Mother lot id对数据进行遍历，并根据遍历过程中Wafer No为1的数据，读出Wafer No, 并将Lot Wafer信息进行写入psmc_lot_wafer数据库中
    for mlot in list_mlot:
        data = df[df.loc[:, 'MLot_ID'] == mlot].copy()  # 按lot生成data数据,包含（MLot_ID，Lot_ID，Current_Chip_Name，Current_Time，Wafer信息）
        data.sort_values(by='Current_Time', axis=0, ascending=False, inplace=True, na_position='first')
        for index, row in data.iteritems():
            if row.name in ['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                            '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25']:
                # todo 按Wafer No对TJS Lot id进行写入
                dictlot = dict()  # 创建字典，用于装载BE信息
                dictlot['Current_Chip_Name'] = str(data['Current_Chip_Name'].values[-1])  # 由于Current_Chip_Name有好几个，选择最后一个
                dictlot['Mlot_ID'] = mlot
                dictlot['Lot_Wafer_No'] = mlot + row.name
                dictlot['Wafer_No'] = row.name
                for i in range(len(row.values)):   # 如果某一片Wafer在不同的lot_id中重复，需要循环重复的次数；
                    if row.values[i] == '1':
                        # todo 连接tjs_wo_tracking_table数据库，按mlot，Wafer No获取每片Wafer的TJS lot id
                        connection = pymysql.connect(**sql_config)
                        with connection.cursor() as cursor:
                            cursor.execute('USE testdb;')
                            cursor.execute(
                                "SELECT FE_Lot_ID, BE_Lot_ID, `Assembly_Config`,`Picking_Sorts`,`%s` FROM tjs_wo_tracking_table WHERE FE_Lot_ID REGEXP '%s' " % (row.name, mlot))
                            sql_results = cursor.fetchall()
                            columnDes = cursor.description
                            columnNames = [columnDes[i][0] for i in range(len(columnDes))]
                            connection.close()
                            #  todo 获取wo中BE_Lot_ID,Picking_Sorts，Wafer No的对应关系
                            for result in sql_results:
                                if result[4] == '1':   # 选取Wafer No为1的bin
                                    for binNo in result[3].split(','):
                                        if binNo.strip() == '01~11':
                                            dictlot['BE_Lot_ID(Bin01~11)'] = result[1]
                                        elif binNo.strip() == '16~21':
                                            dictlot['BE_Lot_ID(Bin16~21)'] = result[1]
                                        else:
                                            dictlot['BE_Lot_ID(Other)'] = result[1]
                        continue   # 只要有一个成立，则跳出for循环
                dflot = pd.DataFrame.from_dict([dictlot], orient='columns')   # 将生成的dictlot信息转化为DataFrame
                dflot = dflot.reindex(columns=['Current_Chip_Name', 'Mlot_ID', 'Lot_Wafer_No', 'Wafer_No', 'BE_Lot_ID(Bin01~11)', 'BE_Lot_ID(Bin16~21)', 'BE_Lot_ID(Other)'], fill_value=np.nan)
                myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
                pd.io.sql.to_sql(dflot, 'psmc_lot_wafer', con=myconnect, schema='testdb', if_exists='append', index=False)


if __name__ == "__main__":
    GenLotWafer()


