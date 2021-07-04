"""
QLable与伙伴控件
mainLayout.addWidget(控件对象, rowIndex, columnIndex, row, column)

"""
import sys
from PyQt5.QtWidgets import *


class QLabelBuddy(QDialog):
    def __init__(self):
        super(QLabelBuddy, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QLable与伙伴控件')

        nameLabel = QLabel('&Name', self)
        nameLineEdit = QLineEdit(self)
        # 设置伙伴控件
        nameLabel.setBuddy(nameLineEdit)

        passwordLabel = QLabel('&Password', self)
        passwordLineEdit = QLineEdit(self)   # 输入单行的文本
        # 设置伙伴控件
        passwordLabel.setBuddy(passwordLineEdit)

        btnOk = QPushButton('&OK')
        btnCancel = QPushButton('&Cannel')

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(nameLineEdit, 0, 1, 1, 2)

        mainLayout.addWidget(passwordLabel, 1, 0)
        mainLayout.addWidget(passwordLineEdit, 1, 1, 1, 2)

        mainLayout.addWidget(btnOk, 2, 1)
        mainLayout.addWidget(btnCancel, 2, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QLabelBuddy()
    main.show()
    sys.exit(app.exec_())


