#!/usr/bin/python
# -*- coding: utf-8 -*-

"""查询xmc wip数据库，并将Setp按工艺顺序提取出来"""
"""
# 1. 将Lot ID提取出来;
# 2. 将Setp 按照Lot IDt提取出来并按时间排序;
# 3. 将两个序列按顺序进行插叙排列
"""

import pandas as pd
from Python_Work.gui_pyqt.mysqlconfig import MySQL

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


def select_lot(productid):
    """将Lot Id从数据库中提取出来"""
    mysql = MySQL()
    mysql.selectDb('testdb')
    Lotid = []
    for Pid in productid:
        sql = "SELECT DISTINCT MLot_ID FROM xmc_wip_tracing_table WHERE Current_Chip_Name = '%s'" % Pid
        desc, result = mysql.sqlAll(sql)
        Lotid = Lotid + [result[i][0] for i in range(len(result))]
    mysql.cur.close()
    return Lotid


def select_layer(product_layer):
    """将当前的step从数据库中提取出来"""
    mysql = MySQL()
    mysql.selectDb('product_layer')
    sql = "SELECT * FROM %s" % product_layer
    desc, result = mysql.sqlAll(sql)
    df = pd.DataFrame(result, columns=desc)
    mysql.cur.close()
    return df


def get_product():
    """将Lot Id从数据库中提取出来"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT DISTINCT Product_Layer FROM xmc_product_version"
    desc, result = mysql.sqlAll(sql)
    mysql.cur.close()
    return [result[i][0] for i in range(len(result))]


def get_productId(product):
    mysql = MySQL()
    mysql.selectDb('configdb')
    sql = "SELECT XMC_Product_ID FROM xmc_product_version WHERE Product_Layer = '%s'" % product
    desc, result = mysql.sqlAll(sql)
    mysql.cur.close()
    return [result[i][0] for i in range(len(result))]


def check_dif(data1, data2):
    """将data1的数据与data2的不同数据合并，不同的放在后面，相同的删除，并返回合并后的data"""
    data1["No1"] = data1.index
    data2["No2"] = data2.index
    data1 = data1.append(data2)
    data1.drop_duplicates(subset=['Layer'], keep='first', inplace=True)
    data1.drop(['No1', 'No2'], axis=1, inplace=True)
    return data1


def check_same(data1, data2):
    """根据data2中的顺序，确认data1的顺序是否匹配data2，如果不匹配，则将不匹配的地方进行调整，并返回调整后的data"""
    data1["No1"] = data1.index
    data2["No2"] = data2.index
    result = pd.merge(data1, data2, how='left', on='Layer')
    # print(result)
    row = 0
    totalrow = result.shape[0]    # 给出行数
    while row < totalrow:
        if not (pd.isnull(result.iloc[row]['No2']) or pd.isnull(result.iloc[row:]['No2'].idxmin())):
            # ---- 当前No2的值不为NaN, 且后续的所有No2的最小值为NaN ----
            while result.iloc[row]['No2'] > result.iloc[result.iloc[row:]['No2'].idxmin()]['No2']:
                # ---- 如果当前No2的数值比后面的No2序列中的最小值大,则把最小值插入到当前位置 ----
                df3 = result.iloc[result.iloc[row:]['No2'].idxmin()]  # 将最小的值赋值给df3
                result.drop([result.iloc[row:]['No2'].idxmin()], inplace=True)     # 删除最小值所对应的行
                df1 = result.loc[:row-1]
                df2 = result.loc[row:]
                result = df1.append(df3, ignore_index=True).append(df2, ignore_index=True)
                result.index = range(0, len(result))
        row = row + 1
    result.drop(['No1', 'No2'], axis=1, inplace=True)
    return result


def steprank():
    # ---- 获取库中的产品清单 ----
    product_layer_list = get_product()
    for product_layer in product_layer_list:    # 对每一种产品进行遍历

        # ---- 获取数据库中的step信息 ----
        current_step = select_layer(product_layer)    # 将当前数据库中的step提取出来
        current_step.drop_duplicates(subset=['Layer'], keep='first', inplace=True)    # 去除库中重复的Layer名称
        current_step.sort_values(by='No', inplace=True)   # 按照layer No大小重新排序
        del current_step['No']

        # ---- 获取数据库中的Lot_Id ----
        product_id = get_productId(product_layer)  # 根据Product_layer获取相应的product_id
        lot_id_list = select_lot(product_id)    # 根据product_id获取Lot_Id
        mysql = MySQL()
        mysql.selectDb('testdb')
        for lot in lot_id_list:
            desc, result = mysql.fetchAll(tbname='xmc_wip_tracing_table', items=['Stage', 'Current_Time', '#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10', '#11', '#12', '#13',
                                                                                 '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'],
                                          condition={'Mlot_id': [lot], 'Current_Chip_Name': product_id})
            df = pd.DataFrame(result, columns=desc)

            # ---- 按Wafer刻号对Step进行遍历
            for indexs in df.columns[2:]:
                data = df[df[indexs] == 1.0].copy()
                if data.empty is not True:
                    # data['Stage'] = data['Stage'].apply(lambda x: x.rstrip(string.digits)) # 去掉Step最后的数字
                    data.drop_duplicates(subset=['Stage'], keep='first', inplace=True)
                    data.sort_values(by='Current_Time', inplace=True)
                    data.index = range(0, len(data))  # 按时间排序后的结果生成index
                    data.drop(['Current_Time', '#01', '#02', '#03', '#04', '#05', '#06', '#07', '#08', '#09', '#10', '#11', '#12', '#13', '#14',
                               '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25'], axis=1, inplace=True)
                    data = data.rename(columns={'Stage': 'Layer'})
                    current_step = check_dif(current_step, data)
                    current_step = check_same(current_step, data)
        # ---- 写入更新后的step到product_layer数据库 ----
        stepsql = MySQL(database='product_layer')
        pd.io.sql.to_sql(current_step, product_layer, con=stepsql.engine, index=True, index_label='No', if_exists='replace')


if __name__ == '__main__':
    steprank()
