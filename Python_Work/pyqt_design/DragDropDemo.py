"""
让控件支持拖拽动作

A. setDragEnAbled(True)

B. setAcceptDrops(True)

B 需要两个事件
1. dragEnterEvent   将A拖拽到B出发
2. dropEvent  在B的区域放下A时触发

"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyComboBox(QComboBox):
    def __init__(self):
        super(MyComboBox, self).__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)
        if e.mimeData().hasText():    # mimeData() - 返回拖放过程中传输数据的QMimeData 对象
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())


class DragDropDemo(QWidget):
    def __init__(self):
        super(DragDropDemo, self).__init__()
        self.setWindowTitle('拖拽案例')
        formLayout =QFormLayout()

        formLayout.addRow(QLabel('请将坐标的文本拖拽到右边的下拉列表中'))

        lineEdit = QLineEdit()
        lineEdit.setDragEnabled(True)

        combo = MyComboBox()

        formLayout.addRow(lineEdit, combo)

        self.setLayout(formLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DragDropDemo()
    main.show()
    sys.exit(app.exec_())



