#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MainWidget import MainWidget
from ui_login import Ui_Dialog


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("UniIC颗粒查询系统")
        self.iniUI()
        QMetaObject.connectSlotsByName(self)

    def iniUI(self):

        self.setCentralWidget(MainWidget())
        self.__creatMenuBar()
        self.__creatToolBar()
        self.__creatStatusBar()
        self.SetScreen()  # 设置窗口大小


    def __creatMenuBar(self):
        manubar = self.menuBar()
        file = manubar.addMenu("File")
        Edit = manubar.addMenu("Edit")
        view = manubar.addMenu("View")
        Tools = manubar.addMenu("Tools")

        logIn = file.addAction("logIn")
        logIn.setObjectName("logIn")
        logIn = file.addAction("Open")
        logIn.setObjectName("Open")


    def __creatToolBar(self):
        layout = QVBoxLayout()
        toolbar = self.addToolBar('TOOLBAR')
        new1 = QAction(QIcon('../pyqt_design/images/Bird.ico'), "Current Wip", self)
        toolbar.addAction(new1)
        open1 = QAction(QIcon('../pyqt_design/images/Cat.ico'), 'Wip History', self)
        toolbar.addAction(open1)
        self.setLayout(layout)

    def __creatStatusBar(self):
        status = self.statusBar()              # 创建状态栏，并悬停5s
        status.showMessage('状态栏', 5000)

    def SetScreen(self):  # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        screen = QApplication.desktop().screenGeometry()  # 获取屏幕的分辨率
        width = int(screen.width())
        height = int(screen.height())
        self.setGeometry(0, 0, width, height-75)

# ============== 自定义功能函数 ============

# ========== 由connectSlotsByName() 自动连接的槽函数==================
    @pyqtSlot()
    def on_logIn_triggered(self):
        self.loginDialog = Ui_Dialog()
        self.loginDialog.setWindowModality(Qt.ApplicationModal)
        self.loginDialog.exec_()
        print(self.label_3)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'../component/images/jpg/08.JPG'))   # 应用程序的图标设置
    main = MainWindows()

    main.show()
    sys.exit(app.exec_())
