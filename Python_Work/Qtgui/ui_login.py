# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()

        # ==== 窗口设置 ====
        self.setWindowTitle("Login Window")
        self.setWindowIcon(QIcon(r'../component/images/jpg/110.JPG'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 使窗口只有一个关闭按钮

        # ==== 设置窗口控件 ====
        self.DiaWidget = QWidget(self)
        self.DiaWidget.setGeometry(QRect(30, 10, 300, 120))

        self.gridLayout = QGridLayout(self.DiaWidget)

        self.verticalLayout_1 = QHBoxLayout(self.DiaWidget)
        self.label_1 = QLabel('dbType:')
        self.comboBox = QComboBox()
        self.comboBox.addItem('Local')
        self.comboBox.addItem('Server')

        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 4)

        self.label_2 = QLabel('user:')
        self.lineEdit_1 = QLineEdit()
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEdit_1, 1, 1, 1, 4)

        self.label_3 = QLabel('database:')
        self.lineEdit_2 = QLineEdit()
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 4)

        self.label_4 = QLabel('password:')
        self.lineEdit_3 = QLineEdit()
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 4)

        self.label_1.setBuddy(self.comboBox)
        self.label_2.setBuddy(self.lineEdit_1)
        self.label_3.setBuddy(self.lineEdit_2)
        self.label_4.setBuddy(self.lineEdit_3)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Ui_Dialog()
    main.show()
    sys.exit(app.exec_())
