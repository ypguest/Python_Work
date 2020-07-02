#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
本脚本用于生成psmc_lot_start数据, 以及psmc_lot_at_wh数据
"""


import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine


# -------根据psmc_wip_report按Lot整理出Lot_Tracing_Table, 要求实施可以更新当前Product ID, Qty, 当前layer, 预期/实际shipping时间-------------
class AutoProcessData(object):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)

    def PsmcLotTracingTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute('USE testdb;')
            cursor.execute("SELECT MLot_ID, Lot_ID, `Current_Chip_Name`,`Current_Time`, Qty, `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, "
                           "`#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` FROM psmc_wip_report WHERE")

            cursor.execute("SELECT Wafer_Start_Date, Lot_ID, MLot_ID, Qty, `Current_Time` FROM psmc_wip_report WHERE Layer = '1F' ORDER BY `Current_time` ASC;")
            sql_results = cursor.fetchall()
            columnDes = cursor.description
            self.connection.close()
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]
        df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)
        myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
        for index, row in df.iterrows():
            # noinspection PyBroadException
            try:
                Lot_start = pd.DataFrame(row[:-1]).T
                pd.io.sql.to_sql(Lot_start, 'psmc_lot_start', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:
                continue


def LotAtWH():
    # Todo 确认每个lot在WH的时间以及Wafer Count;
    lot_id = {}
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    with connection.cursor() as cursor:
        cursor.execute('USE testdb;')
        cursor.execute("SELECT MLot_ID, Lot_ID, `Current_Chip_Name`,`Current_Time`, Qty, `#01`, `#02`, `#03`, `#04`, `#05`, `#06`, `#07`, `#08`, `#09`, `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, "
                       "`#16`, `#17`, `#18`, `#19`, `#20`, `#21`, `#22`, `#23`, `#24`, `#25` FROM psmc_wip_report WHERE TO_DAYS(`Current_Time`) = TO_DAYS(`Forecast_Date`) ORDER BY `Current_time` ASC;")
        sql_results = cursor.fetchall()
        columnDes = cursor.description
        connection.close()
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]             # 获取表头
    df = pd.DataFrame([list(i) for i in sql_results], columns=columnNames)     # 将从数据库中取出的元祖数据转换为dataframe
    df.drop_duplicates(subset=['Lot_ID'], keep='first', inplace=True)          # 将dataframe中Lot_id相同的数据，只保留第一次的
    list_mlot = list(df['MLot_ID'].drop_duplicates())                          # 提取出所有数据中唯一的MLOT_ID
    for mlot in list_mlot:
        data = df[df.loc[:, 'MLot_ID'] == mlot].copy()
        data.sort_values(by='Current_Time', axis=0, ascending=False, inplace=True, na_position='first')
        # todo 遍历每一列，如果当列第一个为1，则后续不得为1
        for index, row in data.iteritems():
            if row.name in ['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10',
                            '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25']:
                # todo 按#01,#02 ....#25 Wafer进行重复性确认，如果重复赋值为None
                for i in range(len(row.values)):
                    if row.values[i] == '1':
                        row.values[i+1:] = None
            temp = data[['#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18',
                         '#19', '#20', '#21', '#22', '#23', '#24', '#25']].astype(dtype=float)
            data['Qty'] = temp.sum(axis=1, skipna=np.nan)
        myconnect = create_engine('mysql+mysqldb://root:yp*963.@localhost:3306/testdb?charset=utf8')
        for index, row in data.iterrows():
            # noinspection PyBroadException
            try:
                lot_at_wh = pd.DataFrame(row).T
                pd.io.sql.to_sql(lot_at_wh, 'psmc_lot_at_wh', con=myconnect, schema='testdb', if_exists='append', index=False)
            except Exception:
                continue


if __name__ == "__main__":
    LotStart()
    LotAtWH()


