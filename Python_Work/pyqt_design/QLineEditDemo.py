"""
QLineEdit综合案例
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QLineEditDemo(QWidget):
    def __init__(self):
        super(QLineEditDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QLineEdit综合案例")

        edit1 = QLineEdit()
        # 使用int校验器
        edit1.setValidator(QIntValidator())
        edit1.setMaxLength(4)  # 不超过4位
        edit1.setAlignment(Qt.AlignRight)  # 右对齐
        edit1.setFont(QFont('Arial', 20))  # 设置字体

        edit2 = QLineEdit()
        edit2.setValidator(QDoubleValidator(0.99, 99.99, 2))

        edit3 = QLineEdit()
        edit3.setInputMask("000.000.000.000;_")

        edit4 = QLineEdit()
        edit4.textChanged.connect(self.textChanged)     # 设置输入变化的槽

        edit5 = QLineEdit()
        edit5.setEchoMode(QLineEdit.Password)            # 设置回显模式为Password
        edit5.editingFinished.connect(self.enterPress)   # 设置输入结束的槽

        edit6 = QLineEdit("Hello PyQt5")
        edit6.setReadOnly(True)

        formLayout = QFormLayout()    # 表单布局
        formLayout.addRow("整数校验", edit1)
        formLayout.addRow("浮点数校验", edit2)
        formLayout.addRow("Input Mask", edit3)
        formLayout.addRow("文本变化", edit4)
        formLayout.addRow("密码", edit5)
        formLayout.addRow("只读", edit6)
        self.setLayout(formLayout)

    @staticmethod
    def textChanged(self, text):
        print("输入的内容"+text)

    @staticmethod
    def enterPress(self):
        print('已输入值')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QLineEditDemo()
    main.show()
    sys.exit(app.exec_())
