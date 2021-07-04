"""
合并单元格

setspan(row, col, 要合并的行数，要合并的列数)
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ColumnSort(QWidget):
    def __init__(self):
        super(ColumnSort, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("设置单元格的对其方式")
        self.resize(430, 230)
        layout = QVBoxLayout()

        tableWidget = QTableWidget()
        tableWidget.setRowCount(4)
        tableWidget.setColumnCount(3)
        layout.addWidget(tableWidget)

        # 设置行的标签
        tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重（kg）'])

        newItem = QTableWidgetItem('雷神')
        tableWidget.setItem(0, 0, newItem)
        tableWidget.setSpan(0, 0, 3, 1)

        newItem = QTableWidgetItem('男')
        tableWidget.setItem(0, 1, newItem)
        tableWidget.setSpan(0, 1, 2, 1)

        newItem = QTableWidgetItem('160')
        tableWidget.setItem(0, 2, newItem)
        tableWidget.setSpan(0, 2, 4, 1)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ColumnSort()
    main.show()
    sys.exit(app.exec_())