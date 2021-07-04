#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Python_Work.GuiScrip.my_SqlConfig import MySQL, MySQLite

# plt设置
plt.style.use('ggplot')    # R语言风格

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行

def history_query(lot_id):
    """根据Lot id返回lot histroy相关信息(psmc)"""
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    desc, result = mysql.fetchAll(tbname='psmc_wip_tracing_table', items='*', condition=({'Mlot_ID': lot_id}))
    data = pd.DataFrame(result, columns=desc)
    data['Current_Time'] = data['Current_Time'].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))  # 将日期改为整天，转换为字符strftime('%Y-%m-%d')
    return data


def history_query1(lot_id):
    """根据Lot id返回lot histroy相关信息(xmc)"""
    mysql = MySQL()
    mysql.selectDb('testdb')  # 连接数据库
    desc, result = mysql.fetchAll(tbname='xmc_wip_tracing_table', items='*', condition=({'Mlot_ID': lot_id}))
    data = pd.DataFrame(result, columns=desc)
    data['Current_Time'] = data['Current_Time'].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))  # 将日期改为整天，转换为字符strftime('%Y-%m-%d')
    return data


def layer_query(product):
    """根据Lot所涉及到的product_id，查询涉及的stage顺序信息(psmc)"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    desc, result = mysql.fetchAll(tbname='psmc_product_version', items=['PSMC_Product_ID', 'Product_Layer', ], condition=({'PSMC_Product_ID': product}))
    product_layers = pd.DataFrame(result, columns=desc)  # 获得该Lot所涉及到的layer库名称

    return product_layers


def layer_query1(product):
    """根据Lot所涉及到的product_id，查询涉及的stage顺序信息(xmc)"""
    mysql = MySQL()
    mysql.selectDb('configdb')
    desc, result = mysql.fetchAll(tbname='xmc_product_version', items=['XMC_Product_ID', 'Product_Layer', ], condition=({'XMC_Product_ID': product}))
    product_layers = pd.DataFrame(result, columns=desc)  # 获得该Lot所涉及到的layer库名称
    print(product)
    return product_layers


def draw_history(lot_id, fab_code):
    # ---- 初始化变量 ----
    im = 0    # 图层变量

    # ---- 根据Lot id返回lot histroy相关信息 ----
    if fab_code == 'psmc':
        data = history_query(lot_id)
    elif fab_code == 'xmc':
        data = history_query1(lot_id)
    product_id = data['Current_Chip_Name'].unique()   # 提取出该Lot涉及的product信息

    # ---- 根据Lot所涉及到的product_id，查询涉及的stage顺序信息 ----
    if fab_code == 'psmc':
        product_layers = layer_query(product_id)
    elif fab_code == 'xmc':
        product_layers = layer_query1(product_id)
    print(product_layers)
    # ---- 将layer生成不重复的list ----
    product_layer_list = product_layers['Product_Layer'].tolist()
    product_layer_list = list(set(product_layer_list))
    print(product_layer_list)

    # ---- 创建图层 ----
    fig, ax = plt.subplots(nrows=len(product_layer_list), ncols=1, sharex='col')

    # ---- 根据product_layer信息生成wip信息 ----
    for product_layer in product_layer_list:
        # ---- 根据product_layer查找产品名称列表 ----
        if fab_code == 'psmc':
            product_list = product_layers['PSMC_Product_ID'].loc[product_layers['Product_Layer'] == product_layer].tolist()
        elif fab_code == 'xmc':
            product_list = product_layers['XMC_Product_ID'].loc[product_layers['Product_Layer'] == product_layer].tolist()
        re_data = data.loc[data['Current_Chip_Name'].isin(product_list)].copy()


        # ---- 给出当前产品所涉及到的stage信息 ----
        layersql = MySQL()
        layersql.selectDb('product_layer')
        desc, result = layersql.fetchAll(tbname=product_layer)
        stage = pd.DataFrame(result,  columns=desc)
        stage = stage.rename(columns={'Layer': 'Stage'})

        # ---- 筛选出Lot ID ----
        lots_id = re_data['Lot_ID'].unique()

        for lot in lots_id:

            draw_data = re_data.loc[re_data['Lot_ID'] == lot].copy()   # 按Lot_ID对数据进行筛选
            draw_data.sort_values(by='Current_Time', inplace=True)  # 按照Current_Time排序
            draw_data = pd.merge(stage, draw_data, on='Stage', how='right')    # 将stage信息与Lot history进行合并

            if len(product_layer_list) == 1:

                # ---- 对数据进行画图 ----
                ax.plot(draw_data['Current_Time'], draw_data['No'], marker='o', linestyle='-', label=lot, linewidth=2)

                # ---- 坐标轴设置 ----
                ax.set(xlim=(data['Current_Time'].min(), data['Current_Time'].max()), ylim=(stage['No'].min(), stage['No'].max()), ylabel=product_layer)

                # ---- 使用set_yticks和set_yticklabels设置刻度 ----
                ax.set_yticks(stage['No'].tolist())
                ax.set_yticklabels(stage['Stage'].tolist(), fontsize='small')

                # ---- 设置X坐标轴旋转 ----
                for tick in ax.get_xticklabels():
                    tick.set_rotation(270)

                # ---- 主刻度设置 ----
                ax.yaxis.set_major_locator(plt.MaxNLocator(10))
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

            else:

                # ---- 对数据进行画图 ----
                ax[im].plot(draw_data['Current_Time'], draw_data['No'], marker='o', linestyle='-', label=lot, linewidth=2)

                # ---- 坐标轴设置 ----
                ax[im].set(xlim=(data['Current_Time'].min(), data['Current_Time'].max()),
                           ylim=(stage['No'].min(), stage['No'].max()), ylabel=product_layer)

                # ---- 使用set_xticks和set_xticklabels设置刻度 ----
                ax[im].set_yticks(stage['No'].tolist())
                ax[im].set_yticklabels(stage['Stage'].tolist(), fontsize='small')

                for tick in ax[im].get_xticklabels():
                    tick.set_rotation(270)

                # ---- 主刻度设置 ----
                ax[im].yaxis.set_major_locator(plt.MaxNLocator(10))
                ax[im].xaxis.set_major_locator(plt.MaxNLocator(10))
                ax[im].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        im = + 1

    plt.subplots_adjust(hspace=0.1)
    plt.show()


if __name__ == '__main__':
    selected_id = ['PPB354']    # PB1986
    fab = 'xmc'
    draw_history(selected_id, fab)
