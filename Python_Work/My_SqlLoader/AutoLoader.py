# ///////////////////////////////////////////////////////////////
#
# BY: Jason Yin
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

# !/usr/bin/python
# -*- coding: utf-8 -*-

# 导入标准库
from time import strftime, localtime

# 导入本地模块
from Python_Work.My_SqlLoader.psmclotloader import PsmcLotLoader
from Python_Work.My_SqlLoader.xsmclotloader import XmcLotLoader

# 函数设置
# /////////////////////////////


def main1():
    file_path = r'F:\08 Daily_Report\01_PTC_Wip'
    PsmcLotLoader(file_path)


if __name__ == "__main__":
    while True:
        time_now = strftime("%H:%M:%S", localtime())  # 刷新
        if time_now == '21:00:00':
            main1()
            time.sleep(300)
