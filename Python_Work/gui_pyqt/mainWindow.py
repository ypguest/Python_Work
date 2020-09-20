#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Python_Work.gui_pyqt.MainWidget import MainWidget


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.iniUI()
        self.MenuBar()
        self.ToolBar()
        self.setCentralWidget(MainWidget())

    def iniUI(self):
        self.setWindowTitle("UniIC颗粒查询系统")
        self.SetScreen()  # 设置窗口大小

    def MenuBar(self):
        layout = QHBoxLayout()
        manubar = self.menuBar()
        file = manubar.addMenu("File")
        Edit = manubar.addMenu("Edit")
        view = manubar.addMenu("View")
        Tools = manubar.addMenu("Tools")
        self.setLayout(layout)

    def ToolBar(self):
        layout = QVBoxLayout()
        toolbar = self.addToolBar('TOOLBAR')
        new1 = QAction(QIcon('../pyqt_design/images/Bird.ico'), "Current Wip", self)
        toolbar.addAction(new1)
        open1 = QAction(QIcon('../pyqt_design/images/Cat.ico'), 'Wip History', self)
        toolbar.addAction(open1)
        self.setLayout(layout)

    def StatusBar(self):
        status = self.statusBar()              # 创建状态栏，并悬停5s
        status.showMessage('状态栏', 5000)

    def SetScreen(self):  # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        screen = QApplication.desktop().screenGeometry()  # 获取屏幕的分辨率
        width = int(screen.width())
        height = int(screen.height())
        self.setGeometry(0, 0, width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'../pyqt_design/images/UniIC_Logo.ico'))   # 应用程序的图标设置
    main = MainWindows()
    main.show()
    sys.exit(app.exec_())
