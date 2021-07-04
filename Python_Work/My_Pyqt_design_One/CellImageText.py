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


class CellImage(QWidget):
    def __init__(self):
        super(CellImage, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("在单元格中实现图文混排的效果")
        self.resize(430, 230)
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(4)
        layout.addWidget(self.tableWidget)

        # 设置行的标签
        self.tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重（kg）', '显示图片'])

        newItem = QTableWidgetItem('雷神')
        self.tableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem('男')
        self.tableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem('160')
        self.tableWidget.setItem(0, 2, newItem)

        newItem = QTableWidgetItem(QIcon('./images/Bird.ico'), 'Bird')
        self.tableWidget.setItem(0, 3, newItem)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CellImage()
    main.show()
    sys.exit(app.exec_())