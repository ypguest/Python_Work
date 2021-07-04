# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class logInWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('UniIC登陆界面')

        # ==== 置输入的用户名 ====
        nameLabel = QLabel('用户名: ', self)               # 输入用户名
        nameLabel.setAlignment(Qt.AlignRight)             # 设置字体右对齐
        nameLabel.setFont(QFont('等线', 15))               # 设置字体

        nameLineEdit = QLineEdit(self)                     # 输入单行的文本
        nameLineEdit.setPlaceholderText("请输入用户名")     # 设置文本框悬浮文字
        nameLineEdit.setFont(QFont('等线', 15))  # 设置字体
        nameLineEdit.setClearButtonEnabled(True)    # 设置显示清除按钮

        nameLabel.setBuddy(nameLineEdit)        # 设置伙伴控件， 即按Alt+N可以切换到QLabel关联的文本框

        # todo 设置输入的密码
        passwordLabel = QLabel('密码: ', self)     # 输入密码
        passwordLabel.setFont(QFont('等线', 15))  # 设置字体
        passwordLabel.setAlignment(Qt.AlignRight)  # 设置字体右对齐
        passwordLineEdit = QLineEdit(self)
        passwordLineEdit.setPlaceholderText("请输入密码")
        passwordLineEdit.setFont(QFont('等线', 15))  # 设置字体
        passwordLineEdit.setClearButtonEnabled(True)  # 设置显示清除按钮
        passwordLineEdit.setEchoMode(QLineEdit.Password)    # 设置回显模式
        passwordLabel.setBuddy(passwordLineEdit)

        btnOk = QPushButton('OK')
        btnCancel = QPushButton('Cannel')

        # 采用栅格布局进行布局
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(nameLineEdit, 0, 1, 1, 2)

        mainLayout.addWidget(passwordLabel, 1, 0)
        mainLayout.addWidget(passwordLineEdit, 1, 1, 1, 2)

        mainLayout.addWidget(btnOk, 2, 1)
        mainLayout.addWidget(btnCancel, 2, 2)

        btnOk.clicked.connect(lambda: self.btnok_cliked(nameLineEdit, passwordLineEdit))

    @staticmethod
    def btnok_cliked(nameLineEdit, passwordLineEdit):
        username = nameLineEdit.text()
        password = passwordLineEdit.text()
        print(username, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = logInWindow()
    main.show()
    sys.exit(app.exec_())



