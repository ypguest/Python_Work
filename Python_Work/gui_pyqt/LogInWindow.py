#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class LogInWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('UniIC登陆界面')

        nameLabel = QLabel('&Name', self)       # 输入用户名
        nameLineEdit = QLineEdit(self)          # 输入单行的文本
        nameLabel.setBuddy(nameLineEdit)        # 设置伙伴控件， 即按Alt+N可以切换到QLabel关联的文本框

        passwordLabel = QLabel('&Password', self)     # 输入密码
        passwordLineEdit = QLineEdit(self)
        passwordLabel.setBuddy(passwordLineEdit)

        btnOk = QPushButton('&OK')
        btnCancel = QPushButton('&Cannel')

        # 采用栅格布局进行布局
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(nameLineEdit, 0, 1, 1, 2)

        mainLayout.addWidget(passwordLabel, 1, 0)
        mainLayout.addWidget(passwordLineEdit, 1, 1, 1, 2)

        mainLayout.addWidget(btnOk, 2, 1)
        mainLayout.addWidget(btnCancel, 2, 2)

        btnOk.clicked.connect(self.btnok_cliked)

    def btnok_cliked(self):
        print('ok')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = LogInWindow()
    main.show()
    sys.exit(app.exec_())
