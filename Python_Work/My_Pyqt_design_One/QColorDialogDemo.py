"""
字体, 背景颜色对话框： QColorDialog
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QColorDialogDemo(QWidget):
    def __init__(self):
        super(QColorDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ColorDialog例子')
        layout = QVBoxLayout()

        self.colorbutton1 = QPushButton('选择字体颜色')
        self.colorbutton1.clicked.connect(self.getColor)
        layout.addWidget(self.colorbutton1)

        self.colorbutton2 = QPushButton('选择背景颜色')
        self.colorbutton2.clicked.connect(self.getColor)
        layout.addWidget(self.colorbutton2)

        self.colorLabel = QLabel('Hello, 测试字体例子')
        layout.addWidget(self.colorLabel)

        self.setLayout(layout)

    def getColor(self):
        color = QColorDialog.getColor()     # 显示颜色对话框
        palette1 = QPalette()  # 实例化调色板QPalette类, 专门用于管理控件的外观显示,可用于设置背景颜色，背景图片
        if self.sender().text() == '选择字体颜色':
            palette1.setColor(QPalette.WindowText, color)   # 颜色器设置颜色
            self.colorLabel.setPalette(palette1)  # 让颜色器上的颜色整合到label上去
        elif self.sender().text() == '选择背景颜色':
            palette1.setColor(QPalette.Window, color)   # 颜色器设置颜色
            self.colorLabel.setAutoFillBackground(True)  # 允许对背景色进行修改
            self.colorLabel.setPalette(palette1)  # 让颜色器上的颜色整合到label上去


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QColorDialogDemo()
    main.show()
    sys.exit(app.exec_())


