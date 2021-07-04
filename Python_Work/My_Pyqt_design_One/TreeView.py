"""
QTreeView控件与系统定制模式

使用Model进行装载
QDirModel 用于显示当前操作系统的目录结构

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = QDirModel()     # 用于显示树状结构的模型
    tree = QTreeView()
    tree.setModel(model)    # 将QDirModel放入树状model中
    tree.setWindowTitle('QTreeView')
    tree.show()
    sys.exit(app.exec_())
