"""
在表格中显示上下文菜单
1. 如何弹出菜单
2. 如何在满足条件（如何判断条件，如果不满足条件，则不能弹出菜单）的情况下弹出菜单

需要使用QMenu的exec_方法

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
        self.setWindowTitle("在表格中显示上下文菜单")
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

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)    # 允许tableWidget单击右键, 响应一个事件, 弹出菜单
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)    # 将定制上下文菜单的信号请求连接到槽

        self.setLayout(layout)

    def generateMenu(self, pos):
        print(pos)
        for i in self.tableWidget.selectionModel().selection().indexes():        # 判断当前单击的是哪一行，以最后选择的一行为主
            rowNum = i.row()         # 返回当前选择行的索引

        # 如果选择的行索引小于2，弹出上下文菜单
        if rowNum < 2:
            menu = QMenu()    # 创建上下文菜单
            item1 = menu.addAction("菜单项1")
            item2 = menu.addAction("菜单项2")
            item3 = menu.addAction("菜单项3")

            # 将坐标转换为菜单坐标
            screenPos = self.tableWidget.mapToGlobal(pos)

            # 被阻塞
            action = menu.exec(screenPos)    # 显示菜单
            if action == item1:
                print('选择了第一个菜单项',
                      self.tableWidget.item(rowNum, 0).text(),
                      self.tableWidget.item(rowNum, 1).text(),
                      self.tableWidget.item(rowNum, 2).text())
            elif action == item2:
                print('选择了第2个菜单项',
                      self.tableWidget.item(rowNum, 0).text(),
                      self.tableWidget.item(rowNum, 1).text(),
                      self.tableWidget.item(rowNum, 2).text())
            elif action == item3:
                print('选择了第3个菜单项',
                      self.tableWidget.item(rowNum, 0).text(),
                      self.tableWidget.item(rowNum, 1).text(),
                      self.tableWidget.item(rowNum, 2).text())
            else:
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CellImage()
    main.show()
    sys.exit(app.exec_())