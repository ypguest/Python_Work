# !/usr/bin/python
# -*- coding: utf-8 -*-

# 导入标准库
from time import strftime, localtime
from threading import Thread

# 导入本地模块
from Python_Work.My_SqlLoader.psmcwiploader import PsmcWipLoader
from Python_Work.My_SqlLoader.xmcwiploader import XmcWipLoader


# 函数设置
# ///////////////////////////////////////////////////////////////
class SubThread1(Thread):
    def run(self):               # 固定写法
        while True:
            time_now = strftime("%H:%M:%S", localtime())  # 刷新
            if time_now == '20:24:00':
                PsmcWipLoader()


class SubThread2(Thread):
    def run(self):               # 固定写法
        while True:
            time_now = strftime("%H:%M:%S", localtime())  # 刷新
            if time_now == '20:24:00':
                XmcWipLoader()


if __name__ == "__main__":
    t1 = SubThread1()
    t2 = SubThread2()
    t1.start()  # 开启线程
    t2.start()  # 开启线程
