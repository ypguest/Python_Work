# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Python_Work.InkCode.inkwmapdisplayframe import Ui_Dialog
QDir

class InkWmapDisplayDialog(Ui_Dialog):

    def __init__(self):
        super(InkWmapDisplayDialog, self).__init__()
        self.rowCount = int()  # 定义Wafer map的rowCount
        self.columnCount = int()    # 定义Wafer map的columnCount
        self.wafermap = None        # 定义Wafermap数据的存储变量
        self.sortink = None

        # ---- 打开文件夹 ----
        self.pushReadFileName.clicked.connect(self.readFile)
        self.pushButtonAddBinInk.clicked.connect(self.addinkfromwmap)

    def readFile(self):
        """读取WAMP文件，返回Wafer Map的list"""
        fileDialog = QFileDialog()
        filename = fileDialog.getOpenFileName(self, 'Open file', r'C:\Users\yinpeng\Desktop\新建文件夹 (6)',
                                              'Ink Files(*.*)')[0]
        self.wafermap = list()
        with open(filename) as Fopen:
            lines = Fopen.readlines()
            for line in lines:
                if line.strip('\n').startswith('LOTMEA'):
                    lotId = line[7:]
                    print(lotId )
                if line.strip('\n').startswith('MAPID1'):
                    waferNo = line[7:].split('.')[-1].strip('\n')
                    print(waferNo)
                if line.strip('\n').startswith('DESIGN'):
                    productId = line[7:]
                if line.strip('\n').startswith('TIMEST'):
                    testTime = line[7:]
            for line in lines[7:-1]:
                if len(line.strip('\n')[7:-1].rstrip()) == 0:   # 跳出空行
                    continue
                regs = re.finditer(r".{7}", line.strip('\n')[6:-23])   # 将每一行的数据按照7进行分割
                linedata = ''
                for reg in regs:
                    linedata = linedata + reg.group()[1] + reg.group()[2] + reg.group()[4] + reg.group()[5]
                self.wafermap.append(re.findall(r".", linedata))
            self.wafermap = np.array(self.wafermap)
        self.showwamp()

    def showwamp(self):
        """put the selected lot and wafer wmap to the table"""
        # ---------------------- 设置字体 -------------------------------- #
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Arial")
        # ----------------- 设置tablewidget的标题 ------------------------- #
        self.rowCount = self.wafermap.shape[0]    # 获取wmap文件的行数
        self.columnCount = self.wafermap.shape[1]    # 获取wmap文件的列数
        self.tableWidget.setRowCount(self.rowCount)
        self.tableWidget.setColumnCount(self.columnCount)
        self.tableWidget.horizontalHeader().setFont(font)    # 将行标题的字体进行设置
        self.tableWidget.verticalHeader().setFont(font)      # 将列标题的字体进行设置
        self.tableWidget.horizontalHeader().setMinimumSectionSize(7)     # 设置行标题的最小宽度
        self.tableWidget.horizontalHeader().setDefaultSectionSize(7)     # 设置行标题的默认宽度
        self.tableWidget.verticalHeader().setMinimumSectionSize(3)      # 设置行标题的最小宽度
        self.tableWidget.verticalHeader().setDefaultSectionSize(3)      # 设置行标题的默认宽度

        self.tableWidget.horizontalHeader().setVisible(False)   # 将行坐标隐藏
        self.tableWidget.verticalHeader().setVisible(False)     # 将列标隐藏

        self.tableWidget.setFrameShape(QFrame.NoFrame)          # 设置边框
        self.tableWidget.setShowGrid(False)                       # 将列标隐藏

        for i in range(self.rowCount):  # 将数据填入map
            for j in range(self.columnCount):
                item = QTableWidgetItem(self.wafermap[i, j])
                item.setFont(font)
                if self.wafermap[i, j] == '1':   # 当内容为bin1时，设置为绿色
                    item.setBackground(QColor(0, 255, 0))
                if self.wafermap[i, j] == '2':   # 当内容为bin2时，设置为红色
                    item.setBackground(QColor(255, 0, 0))
                if self.wafermap[i, j] == '0':   # 当内容为bin0时，设置为红色
                    item.setBackground(QColor(255, 0, 0))
                if self.wafermap[i, j] == '3':   # 当内容为bin0时，设置为黄色
                    item.setBackground(QColor(255, 255, 0))
                self.tableWidget.setItem(i, j, item)
        print()
        for k in range(self.rowCount):
            self.tableWidget.setRowHeight(k, 1)
        for k in range(self.columnCount):
            self.tableWidget.setColumnWidth(k, 1)
        self.horizontalLayout.addWidget(self.tableWidget)

    def addinkfromwmap(self):
        """对wamp进行ink"""
        passdutinfosHash = {}
        faildutinfosHash = {}
        self.showwamp()
        for i in range(self.rowCount):  # 将数据填入map
            for j in range(self.columnCount):
                if self.wafermap[i, j] == '0':
                    try:
                        faildutinfosHash[i][j] = 2
                    except KeyError:
                        faildutinfosHash[i] = {}
                        faildutinfosHash[i][j] = 2
                if self.wafermap[i, j] == '1':
                    try:
                        passdutinfosHash[i][j] = 0
                    except KeyError:
                        passdutinfosHash[i] = {}
                        passdutinfosHash[i][j] = 0
                if self.wafermap[i, j] == '2':
                    try:
                        faildutinfosHash[i][j] = 2
                    except KeyError:
                        faildutinfosHash[i] = {}
                        faildutinfosHash[i][j] = 2
                if self.wafermap[i, j] == '3':         # Pass bin
                    try:
                        passdutinfosHash[i][j] = 0
                    except KeyError:
                        passdutinfosHash[i] = {}
                        passdutinfosHash[i][j] = 0

        self.sortink = self.findring(faildutinfosHash, passdutinfosHash)
        self.mapink2table(self.sortink)
        self.horizontalLayout.addWidget(self.tableWidget)

    def findring(self, faildutinfosHash, passdutinfosHash):
        '''
        find the ink duts based on the faildutinfosHash ,passdutinfosHash and ring number
        :param faildutinfosHash:
        :param passdutinfosHash:
        :return: the inked dut position
        '''
        ringHash = {}
        ringNums = int(str(self.comboBoxRingNum.currentText()))
        for _i in range(ringNums):
            ringHash[_i] = {}
        for X in faildutinfosHash.keys():
            for Y in faildutinfosHash[X].keys():
                for xoffset, yoffset in zip([1, 0, -1, 0], [0, -1, 0, 1]):
                    try:
                        if faildutinfosHash[X + xoffset][Y + yoffset]:
                            faildutinfosHash[X][Y] += 1
                    except KeyError:
                        pass

        for X in faildutinfosHash.keys():
            for Y in faildutinfosHash[X].keys():
                for xoffset, yoffset in zip([1, 0, -1, 0], [0, -1, 0, 1]):
                    try:
                        if faildutinfosHash[X + xoffset][Y + yoffset] > 4:
                            faildutinfosHash[X][Y] = 5
                    except KeyError:
                        pass

        for X in passdutinfosHash.keys():
            for Y in passdutinfosHash[X].keys():
                for xoffset in [-1, 0, 1]:
                    for yoffset in [-1, 0, 1]:
                        if xoffset == 0 and yoffset == 0:
                            continue
                        try:
                            if faildutinfosHash[X + xoffset][Y + yoffset] > 4:
                                passdutinfosHash[X][Y] = 1
                                try:
                                    ringHash[0][X][Y] = 1
                                except KeyError:
                                    ringHash[0][X] = {}
                                    ringHash[0][X][Y] = 1
                        except KeyError:
                            pass

        for ringNum in range(1, ringNums):
            for X in passdutinfosHash.keys():
                for Y in passdutinfosHash[X].keys():
                    for xoffset in [-1, 0, 1]:
                        for yoffset in [-1, 0, 1]:
                            if xoffset == 0 and yoffset == 0:
                                continue
                            try:
                                if ringHash[ringNum - 1][X - 1][Y] == 1:
                                    try:
                                        ringHash[ringNum][X][Y] = 1
                                    except KeyError:
                                        ringHash[ringNum][X] = {}
                                        ringHash[ringNum][X][Y] = 1
                            except KeyError:
                                pass

        return ringHash

    def mapink2table(self, ringHash):
        ringNums = int(str(self.comboBoxRingNum.currentText()))   # 计算ink几圈
        for _i in range(ringNums):
            self.mapfail2table(ringHash[_i])

    def mapfail2table(self, failhash):
        for X in failhash.keys():
            for Y in failhash[X].keys():
                tableRow = X
                tableCol = Y
                if int(str(self.tableWidget.item(tableRow, tableCol).text())) == 1 or int(str(self.tableWidget.item(tableRow, tableCol).text())) == 3:
                    self.tableWidget.item(tableRow, tableCol).setText('99')
                    self.tableWidget.item(tableRow, tableCol).setBackground(QColor(0, 0, 255))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = InkWmapDisplayDialog()
    main.show()
    sys.exit(app.exec_())
QFont