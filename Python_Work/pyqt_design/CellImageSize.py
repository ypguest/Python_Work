"""
改变单元格中图片的尺寸

setIconSize(Qsize(width, height))

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CellImage(QWidget):
    def __init__(self):
        super(CellImage, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("在单元格中实现图文混排的效果")
        self.resize(430, 230)
        layout = QVBoxLayout()

        tableWidget = QTableWidget()
        tableWidget.setIconSize(QSize(48, 48))
        tableWidget.setColumnCount(3)
        tableWidget.setRowCount(5)
        layout.addWidget(tableWidget)

        # 设置行的标签
        tableWidget.setHorizontalHeaderLabels(['图片1', '图片2', '图片3'])

        # 让列的宽度和图片的宽度相同
        for i in range(3):
            tableWidget.setColumnWidth(i, 48)
        # 让行的高度和图片的高度相同
        for i in range(15):
            tableWidget.setRowHeight(i, 48)

        for k in range(15):
            i = k // 3   # 行
            j = k % 3   # 列
            item = QTableWidgetItem()
            item.setIcon(QIcon('./images/Bird.ico'))
            tableWidget.setItem(i, j, item)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CellImage()
    main.show()
    sys.exit(app.exec_())