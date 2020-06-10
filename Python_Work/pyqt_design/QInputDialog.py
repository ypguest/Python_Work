"""
QInputDialog 输入对话框

1. QInputDialog.getItem  # 用于显示输入列表
2. QInputDialog.getText  # 用于输入文本的
2. QInputDialog.getInt   # 用于输入数字

"""
import sys
from PyQt5.QtWidgets import *


class QInputDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('输入对话框')
        layout = QFormLayout()

        # 用于显示输入列表
        self.button1 = QPushButton('获取列表中的选项')
        self.button1.clicked.connect(self.getItem)
        self.lineEdit1 = QLineEdit()
        layout.addRow(self.button1, self.lineEdit1)

        # 用于输入文本的
        self.button2 = QPushButton('获取字符串')
        self.button2.clicked.connect(self.getText)
        self.lineEdit2 = QLineEdit()
        layout.addRow(self.button2, self.lineEdit2)

        # 用于输入数字
        self.button3 = QPushButton('获取整数')
        self.button3.clicked.connect(self.getInt)
        self.lineEdit3 = QLineEdit()
        layout.addRow(self.button3, self.lineEdit3)

        self.setLayout(layout)

    def getItem(self):
        items = ('C', 'C++', 'Ruby', 'Python', 'Java')
        item, ok = QInputDialog.getItem(self.sender(), '请选择编程语言', '语言列表', items)
        if ok and item:
            self.lineEdit1.setText(item)

    def getText(self):
        text, ok = QInputDialog.getText(self.sender(), '文本输入框', '输入姓名')
        if ok and text:
            self.lineEdit1.setText(text)

    def getInt(self):
        num, ok = QInputDialog.getInt(self.sender(), '整数输入框', '输入数字')
        if ok and str(num):
            self.lineEdit1.setText(str(num))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QInputDialogDemo()
    main.show()
    sys.exit(app.exec_())

