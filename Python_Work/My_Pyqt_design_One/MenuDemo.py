"""
创建和使用菜单
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MenuDemo(QMainWindow):
    def __init__(self):
        super(MenuDemo, self).__init__()
        bar = self.menuBar()   # 获取顶层菜单栏
        # 第一种方法
        file = bar.addMenu('文件')  # 在顶层菜单栏添加菜单

        file.addAction('新建')      # 添加子菜单
        # 第二种方法
        save = QAction('保存', self)   # 先创建动作
        save.setShortcut('Ctrl + S')        # 增加快捷键
        file.addAction(save)          # addAction 的参数可以是名字或动作，如果为动作，则为时间，可以增加槽；
        save.triggered.connect(self.process)

        edit = file.addMenu('Edit')
        edit.addAction('copy')
        edit.addAction('Paste')

        quit = QAction('退出', self)    # 如果要添加动作, 则必须使用QAction
        edit.addAction(quit)
        quit.triggered.connect(self.process)

    def process(self, a):
        print(self.sender().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MenuDemo()
    main.show()
    sys.exit(app.exec_())