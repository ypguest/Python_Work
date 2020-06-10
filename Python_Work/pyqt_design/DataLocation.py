"""
在表格快速定位到特定的行
1. 数据的定位, 查找表格中满足条件的单元格 findItems, 查找所有满足条件的单元格，返回列表
2. 如果找到了满足条件的单元格，会定位到单元格所在的行 setSliderPosition

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
        self.setWindowTitle("在表格中快速定位")
        self.resize(600, 800)

        layout = QHBoxLayout()
        tabelWidget = QTableWidget()
        tabelWidget.setRowCount(40)
        tabelWidget.setColumnCount(4)

        layout.addWidget(tabelWidget)

        for i in range(40):
            for j in range(4):
                itemContent = '(%d, %d)' % (i, j)
                tabelWidget.setItem(i, j, QTableWidgetItem(itemContent))

        self.setLayout(layout)

        # 寻找满足条件的Cell
        text = '(13, 1)'
        items = tabelWidget.findItems(text, Qt.MatchExactly)   # Qt.MatchStartsWith
        if len(items) > 0:
            item = items[0]
            item.setBackground(QBrush(QColor(0, 255, 0)))   # 设置背景色为绿色
            item.setForeground(QBrush(QColor(255, 0, 0)))   # 设置字体为红色

            row = item.row()
            # 定位到制定的行
            tabelWidget.verticalScrollBar().setSliderPosition(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataLocation()
    main.show()
    sys.exit(app.exec_())
