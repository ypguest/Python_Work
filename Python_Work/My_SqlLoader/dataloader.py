#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from Python_Work.wip_gui.psmclotloader import PsmcLotLoader


# ---- 函数设置 ----
# -----------------


def main1():
    file_path = r'F:\08 Daily_Report\01_PTC_Wip'
    PsmcLotLoader(file_path)


if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        if time_now == '21:00:00':
            main1()
            time.sleep(300)
