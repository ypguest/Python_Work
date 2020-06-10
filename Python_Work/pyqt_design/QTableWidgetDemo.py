"""
扩展的表格控件（QTableWidget）

基于QtableView进行了扩展，添加了单元格的方法，可直接将单元格添加入控件中
每一个Cell(单元格)是一个QTableWidgetItem
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QTableWidgetDemo(QWidget):
    def __init__(self):
        super(QTableWidgetDemo, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("QTableWidget演示")
        self.resize(430, 230)
        layout = QHBoxLayout()

        tablewiget = QTableWidget()
        tablewiget.setRowCount(4)
        tablewiget.setColumnCount(3)

        # 设置行的标签
        tablewiget.setHorizontalHeaderLabels(['姓名', '年龄', '籍贯'])
        # 设置垂直头的标签
        tablewiget.setVerticalHeaderLabels(['a', 'b'])

        nameItem = QTableWidgetItem('小明')
        tablewiget.setItem(0, 0, nameItem)

        ageItem = QTableWidgetItem('24')
        tablewiget.setItem(0, 1, ageItem)

        gItem = QTableWidgetItem('上海')
        tablewiget.setItem(0, 1, gItem)

        # 默认为可编辑状态，禁止编辑
        tablewiget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 选择整行显示
        tablewiget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 根据行和列内容调整
        tablewiget.resizeRowsToContents()
        tablewiget.resizeColumnsToContents()

        # 将表格的头进行隐藏
        tablewiget.horizontalHeader().setVisible(False)
        # tablewiget.verticalHeader().setVisible(False)



        # 隐藏表格线
        tablewiget.setShowGrid(False)

        layout.addWidget(tablewiget)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QTableWidgetDemo()
    main.show()
    sys.exit(app.exec_())