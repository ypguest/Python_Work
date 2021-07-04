# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_LoginWidget import Ui_Dialog

class MyLoginWidget(QDialog, Ui_Dialog):
    def __init__(self):
        super(MyLoginWidget, self).__init__()
        self.LoginWidget = Ui_Dialog()
        self.LoginWidget.setupUi(self)
        self.setWindowTitle("Login Window")
        self.setWindowIcon(QIcon(r'../component/images/jpg/110.JPG'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 使窗口只有一个关闭按钮
        self.setFixedSize(self.width(), self.height())   # 禁止调整窗口大小
        self.setFont(QFont("微软雅黑", 8))   # 设置字体及大小
        self.dbType = None
        self.dbname = None
        self.username = None
        self.pwd = None

# ========== 由connectSlotsByName() 自动连接的槽函数==================
    def on_buttonBox_accepted(self):
        self.dbType = self.LoginWidget.dbTypeComboBox.currentText()
        self.dbname = self.LoginWidget.dblineEdit.text()
        self.username = self.LoginWidget.usernameLineEdit.text()
        self.pwd = self.LoginWidget.pwdLineEdit.text()

    def on_buttonBox_rejected(self):
        self.dbType = None
        self.dbname = None
        self.username = None
        self.pwd = None

# ============== 自定义功能函数 ============

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainWindow()
    main.show()
    sys.exit(app.exec_())

