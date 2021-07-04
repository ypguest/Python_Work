"""
设置单元格的对齐方式

setTextAlignment

Qt.AlignRight 右对齐
Qt.AlignBottom 下对其

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

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        layout.addWidget(self.tableWidget)

        # 设置行的标签
        self.tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重（kg）'])

        newItem = QTableWidgetItem('雷神')
        newItem.setTextAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.tableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem('男')
        newItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem('160')
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, newItem)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ColumnSort()
    main.show()
    sys.exit(app.exec_())