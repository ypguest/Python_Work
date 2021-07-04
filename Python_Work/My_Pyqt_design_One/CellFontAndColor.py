"""
设置单元格字体和颜色
字体名称，大小
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DataLocation(QWidget):
    def __init__(self):
        super(DataLocation, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("设置单元格字体和颜色")
        self.resize(430, 230)
        layout = QHBoxLayout()

        tableWidget = QTableWidget()
        tableWidget.setRowCount(4)
        tableWidget .setColumnCount(3)
        layout.addWidget(tableWidget )

        # 设置行的标签
        tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重（kg）'])

        newItem = QTableWidgetItem('雷神')
        newItem.setFont(QFont('Times', 14, QFont.Black))      # 创建QFont
        newItem.setForeground(QBrush(QColor(255, 0, 0)))     # 设置前景色背景颜色
        newItem.setBackground(QBrush(QColor(0, 0, 255)))     # 设置前景色背景颜色

        tableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem('女')
        newItem.setFont(QFont('Times', 14, QFont.Black))      # 创建QFont
        newItem.setForeground(QBrush(QColor(255, 0, 0)))     # 设置前景色背景颜色
        newItem.setBackground(QBrush(QColor(0, 0, 255)))     # 设置前景色背景颜色
        
        tableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem('160')
        newItem.setFont(QFont('Times', 14, QFont.Black))  # 创建QFont
        newItem.setForeground(QBrush(QColor(255, 0, 0)))  # 设置前景色背景颜色
        newItem.setBackground(QBrush(QColor(0, 0, 255)))  # 设置前景色背景颜色

        tableWidget.setItem(0, 2, newItem)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataLocation()
    main.show()
    sys.exit(app.exec_())






