# !/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
from datetime import datetime
import matplotlib.pyplot as plt

# ---- pd设置 ----
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行
# ---- plt设置 ----
plt.style.use('ggplot')    # R语言风格
# ---- regex设置 ----
regex = re.compile("\\[.*\\]")


class ChipmosftData(object):

    def __init__(self, path):
        """读取路径下的wat数据，并返回数据内容，类型，保存路径等信息"""

        data_path = dir_folder(path)
        rawdata_df = pd.DataFrame()
        for ipath in data_path:
            rawreader = pd.read_excel(ipath, sheet_name=0)
            rawdata_df = rawdata_df.append(rawreader)
        print(rawdata_df)

        #
        #     rawdata_df["Test_Time"] = rawdata_df["Test_Time"].apply(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S"))  # 时间转换
        #     # wat_items = list(rawdata_df)[6:]
        #     # left1 = rawdata_df.groupby('Lot_Wafer')['Test_Time'].max()
        #     # right1 = rawdata_df.groupby('Lot_Wafer')[wat_items].mean()
        #     # rawdata_df = pd.merge(left1, right1, right_on='Lot_Wafer', left_index=True, how='outer')
        #     # rawdata_df.sort_values(by=["Test_Time", "Lot_Wafer"], ascending=[True, True], inplace=True)  # 调整数据顺序
        #
        #     self.save_path = os.path.join(path, 'wat_image', 'psmc')
        #     self.wat_type = 'DRAM'
        #     self.rawdata_df = rawdata_df      # 数据
        #     self.spec_df = pd.read_excel(data_path, sheet_name=spec, header=0, index_col=0)    # 规格

def dir_folder(file_path):
    file_paths = []
    for root, dirs, files in os.walk(file_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for file in files:
            if file == "Thumbs.db":   # 省略图片缩略库文件
                continue
            else:
                file_paths.append(os.path.join(root, file))
    return file_paths


if __name__ == '__main__':
    path = r"C:\Users\yinpeng\Desktop\chipmos_ft"
    watdata = ChipmosftData(path=path)


