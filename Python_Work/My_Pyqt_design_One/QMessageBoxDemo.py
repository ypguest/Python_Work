"""
消息对话框： QMessageBox
主要用于如下情况
1. 关于对话框， 无图标，只显示文字，通常显示一个按钮
2. 错误对话框，一般显示两个按钮
3. 警告对话框，一般显示两个按钮
4. 提问对话框，一般显示两个按钮
5. 消息对话框，一般显示两个按钮

这几种对话框主要在显示的图标不同，对话框显示的按钮不一样
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp


class QMessageBoxDemo(QWidget):
    def __init__(self):
        super(QMessageBoxDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QMessageBox案例")
        self.resize(300, 400)
        layout = QVBoxLayout()

        self.button1 = QPushButton()
        self.button1.setText('显示关于对话框')
        self.button1.clicked.connect(self.showDialog)
        layout.addWidget(self.button1)

        self.button2 = QPushButton()
        self.button2.setText('显示消息对话框')
        self.button2.clicked.connect(self.showDialog)
        layout.addWidget(self.button2)

        self.button3 = QPushButton()
        self.button3.setText('显示警告对话框')
        self.button3.clicked.connect(self.showDialog)
        layout.addWidget(self.button3)

        self.button4 = QPushButton()
        self.button4.setText('显示错误对话框')
        self.button4.clicked.connect(self.showDialog)
        layout.addWidget(self.button4)

        self.button5 = QPushButton()
        self.button5.setText('显示提问对话框')
        self.button5.clicked.connect(self.showDialog)
        layout.addWidget(self.button5)

        self.setLayout(layout)

    def showDialog(self):
        text = self.sender().text()
        if text == '显示关于对话框':
            QMessageBox.about(self.sender(), "消息框标题", "这是关于软件的说明")
        elif text == '显示消息对话框':
            reply = QMessageBox.information(self.sender(), '消息', '这是一个消息对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)   # 消息对话框，可以选择Yes 或者No,其中默认为Yes
            print(reply)
        elif text == '显示警告对话框':
            reply = QMessageBox.warning(self.sender(), '警告', '这是一个警告对话框', QMessageBox.SaveAll | QMessageBox.No, QMessageBox.SaveAll)   # 警告对话框
            print(reply)
        elif text == '显示错误对话框':
            reply = QMessageBox.critical(self.sender(), '错误', '这是一个警告对话框', QMessageBox.SaveAll | QMessageBox.No, QMessageBox.SaveAll)  # 错误
            print(reply)
        elif text == '显示提问对话框':
            reply = QMessageBox.question(self.sender(), '提问', '这是一个警告对话框', QMessageBox.Reset | QMessageBox.No, QMessageBox.Reset)  # 提问
            print(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QMessageBoxDemo()
    main.show()
    sys.exit(app.exec_())

