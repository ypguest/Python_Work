"""
创建和使用工具栏
工具栏默认按钮：只显示图表，将文本作为悬停提示展示

工具栏按钮有3种状态， 通过setToolButtonStyle实现
1. 只显示图标
2. 只显示文本
3. 文本和图标均显示
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ToolBarDemo(QMainWindow):
    def __init__(self):
        super(ToolBarDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("工具栏案例")
        self.resize(300, 200)

        tb1 = self.addToolBar('File')

        new = QAction(QIcon('./images/Bird.ico'), "new", self)
        tb1.addAction(new)

        open = QAction(QIcon('./images/Cat.ico'), 'open', self)
        tb1.addAction(open)

        save = QAction(QIcon('./images/Dog.ico'), 'save', self)
        tb1.addAction(save)

        tb2 = self.addToolBar('File1')

        new1 = QAction(QIcon('./images/Bird.ico'), "new", self)
        tb2.addAction(new)

        open1 = QAction(QIcon('./images/Cat.ico'), 'open', self)
        tb2.addAction(open)

        save1 = QAction(QIcon('./images/Dog.ico'), 'save', self)
        tb2.addAction(save)

        tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        tb1.actionTriggered.connect(self.toolbtnPressed)

    @staticmethod
    def toolbtnPressed(self, a):
        print('按下的工具栏按钮是', a.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ToolBarDemo()
    main.show()
    sys.exit(app.exec_())