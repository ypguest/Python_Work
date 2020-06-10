"""
在单元格中放置控件

可在单元格中放置Button, Combo...
setCellWidget  将控件放入单元格中
setItem  将文本添加到单元格中
setStyleSheet 设置控件的样式{QSS}

"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PlaceControllInCell(QWidget):
    def __init__(self):
        super(PlaceControllInCell, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("在单元格中放置控件")
        self.resize(430, 230)
        layout = QHBoxLayout()
        tableWidget = QTableWidget()
        tableWidget.setRowCount(4)
        tableWidget.setColumnCount(3)

        layout.addWidget(tableWidget)

        tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重(kg)'])

        textItem = QTableWidgetItem('小明')
        tableWidget.setItem(0, 0, textItem)

        combox = QComboBox()
        combox.addItem('男')
        combox.addItem('女')
        # combox.addItems(['男', '女'])
        tableWidget.setCellWidget(0, 1, combox)

        modifyButton = QPushButton('修改')
        modifyButton.setDown(True)  # 默认为按下状态
        # QSS(Qt Style Sheet)  Qt的样式,通过QT的语法设置控件的属性
        modifyButton.setStyleSheet('QPushButton{margin:3px}')   # 设置所有QComboBox控件,让其边距为3px
        tableWidget.setCellWidget(0, 2, modifyButton)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = PlaceControllInCell()
    main.show()
    sys.exit(app.exec_())