"""
按钮控件（QPushButton）

QAbstractButton  # 所有按钮的父类

子类按钮
1. QPushButton      # 常规按钮
2. AToolButton      # 工具条按钮
3. QRadioButton     # 单选按钮    V
4. QCheckBox        # 复选按钮

"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QRadioButtonDemo(QWidget):
    def __init__(self):
        super(QRadioButtonDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QRadioButton")
        layout = QHBoxLayout()
        self.button1 = QRadioButton("单选按钮1")
        self.button1.setChecked(True)      # 将按钮1设置为默认选中状态

        self.button1.toggled.connect(self.buttonState)   # 将按钮1的状态与buttonState的槽进行绑定
        layout.addWidget(self.button1)

        self.button2 = QRadioButton("单选按钮2")
        self.button2.toggled.connect(self.buttonState)    # 将按钮1的状态与buttonState的槽进行绑定
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def buttonState(self):
        radioButton = self.sender()
        if radioButton.isChecked() is True:
            print('<' + radioButton.text() + '> 被选中')
        else:
            print('<' + radioButton.text() + '> 被取消选中状态')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QRadioButtonDemo()
    main.show()
    sys.exit(app.exec_())









