"""
QTextEdit控件介绍，获得文本，控制文本
"""

from PyQt5.QtWidgets import *
import sys


class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo, self).__init__()

        # 实例的属性需在__init__内进行定义
        self.textEdit = QTextEdit()                # 多行文本
        self.buttonText = QPushButton("显示文本")
        self.buttonHTML = QPushButton("显示HTML")
        self.buttonToText = QPushButton("获取文本")
        self.buttonToHTML = QPushButton("获取HTML")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTextEdit控件演示")
        self.resize(300, 280)    # 设置尺寸大小

        layout = QVBoxLayout()   # 创建垂直布局，并对目标进行放置
        layout.addWidget(self.textEdit)
        layout.addWidget(self.buttonText)
        layout.addWidget(self.buttonToText)
        layout.addWidget(self.buttonHTML)
        layout.addWidget(self.buttonToHTML)

        self.setLayout(layout)

        # 设置信号与槽
        self.buttonText.clicked.connect(self.onClick_ButtonText)
        self.buttonToText.clicked.connect(self.onClick_ButtonToText)
        self.buttonHTML.clicked.connect(self.onClick_ButtonHTML)
        self.buttonToHTML.clicked.connect(self.onClick_ButtonToHTML)

    def onClick_ButtonText(self):
        self.textEdit.setPlainText("Hello World")      # setPlainText 设置普通文本

    def onClick_ButtonToText(self):
        print(self.textEdit.toPlainText())     # toPlainText 获取普通文本

    def onClick_ButtonHTML(self):
        self.textEdit.setHtml('<font color = "blue" size = "5">Hello World</font>')    # setHtml 设置HTML文本

    def onClick_ButtonToHTML(self):
        print(self.textEdit.toHtml())       # toHtml() 获取HTML文本


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QTextEditDemo()
    main.show()
    sys.exit(app.exec_())