"""
文件对话框： QFileDialog
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QFileDialogDemo(QWidget):
    def __init__(self):
        super(QFileDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件对话框演示')
        layout = QVBoxLayout()

        self.button1 = QPushButton('加载图片')
        self.button1.clicked.connect(self.loadImage)
        layout.addWidget(self.button1)

        self.imageLabel = QLabel()
        layout.addWidget(self.imageLabel)

        self.button2 = QPushButton('加载文本文件')
        self.button2.clicked.connect(self.loadText)
        layout.addWidget(self.button2)

        self.imageLabe2 = QTextEdit()
        layout.addWidget(self.imageLabe2)

        self.setLayout(layout)

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, caption='打开文件', directory='.', filter='图像文件(*.jpg *.png)')
        self.imageLabel.setPixmap(QPixmap(fname))
    def loadText(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFileDialogDemo()
    main.show()
    sys.exit(app.exec_())