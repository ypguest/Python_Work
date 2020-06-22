"""
按钮控件（QPushButton）

QAbstractButton  # 所有按钮的父类

子类按钮
1. QPushButton      # 常规按钮      V
2. AToolButton      # 工具条按钮
3. QRadioButton     # 单选按钮
4. QCheckBox        # 复选按钮

"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QPushButtonDemo(QWidget):
    def __init__(self):
        super(QPushButtonDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QPushButton Demo")

        layout = QVBoxLayout()

        self.button1 = QPushButton("第一个按钮")   # 指定显示的文本, 采用面向对象的方法
        # self.button1.setText("第一个按钮")   第二种方法, 采用setText方法进行
        self.button1.setCheckable(True)    # 设置按钮是否已经被选中
        self.button1.toggle()   # 使按钮可以在不同状态之间切换
        self.button1.clicked.connect(self.buttonState)   # 绑定Button1的状态
        self.button1.clicked.connect(lambda: self.whichButton(self.button1))   # 通过Lambda表达式，强制对Button1进行绑定
        layout.addWidget(self.button1)

        # 在按钮的文本前面显示图像
        self.button2 = QPushButton("图像按钮")
        self.button2.setIcon(QIcon(QPixmap("./images/python.jpg")))
        self.button2.clicked.connect(lambda: self.whichButton(self.button2))
        layout.addWidget(self.button2)

        # 不可用的按钮
        self.button3 = QPushButton("不可用的按钮")
        self.button3.setEnabled(False)
        layout.addWidget(self.button3)

        # 设置常规按钮
        self.button4 = QPushButton("&MyButton")
        self.button4.setDefault(True)
        self.button4.clicked.connect(lambda: self.whichButton(self.button4))
        layout.addWidget(self.button4)

        self.setLayout(layout)

    def buttonState(self):
        if self.button1.isChecked():
            print('按钮1已经被选中')
        else:
            print('按钮1未被选中')

    def whichButton(self, btn):
        print('被单击的按钮是<' + btn.text() + '>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QPushButtonDemo()
    main.show()
    sys.exit(app.exec_())
