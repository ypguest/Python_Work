#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.SetScreen()

        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("UniIC 颗粒查询系统")
        status = self.statusBar()              # 创建状态栏，并悬停5s
        status.showMessage('状态栏', 5000)
        toolbar = self.addToolBar(u'退出')

    def SetScreen(self):  # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()   # 获取屏幕的分辨率
        height = screenRect.height()-500
        width = screenRect.width()-500
        self.setFixedSize(width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'../pyqt_design/images/UniIC_Logo.ico'))   # 应用程序的图标设置
    main = MainWindows()
    main.show()
    sys.exit(app.exec_())
