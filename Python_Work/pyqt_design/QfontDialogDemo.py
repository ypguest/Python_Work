"""
字体对话框： QfontDialog
"""

import sys
from PyQt5.QtWidgets import *


class QfontDialog(QWidget):
    def __init__(self):
        super(QfontDialog, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Font Dialog例子')
        layout = QVBoxLayout()

        self.fontbutton = QPushButton('选择字体')
        self.fontbutton.clicked.connect(self.getFont)
        layout.addWidget(self.fontbutton)

        self.fontlabel = QLabel('Hello, 测试字体例子')
        layout.addWidget(self.fontlabel)

        self.setLayout(layout)

    def getFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.fontlabel.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QfontDialog()
    main.show()
    sys.exit(app.exec_())


