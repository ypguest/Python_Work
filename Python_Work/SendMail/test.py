# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:test.py
# @Time:2021/7/18 12:13
# @Author:Jason_Yin
from multiprocessing import Process
import time
import os


def SubProess():
    for i in range(1000):
        time.sleep(1)
        print(i, f"SubProess子进程,id是{os.getpid()}")


if __name__ == '__main__':
    p = Process(target=SubProess, name='SubProess')
    p.start()
    for i in range(1000):
        time.sleep(1)
        print(i, f"主进程,id是{os.getpid()}")