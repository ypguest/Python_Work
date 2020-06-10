"""
树控件(QTreeWidget)的基本用法

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class BasicTreeWidget(QMainWindow):
    def __init__(self):
        super(BasicTreeWidget, self).__init__()
        self.setWindowTitle("为树节点添加响应的事件")
        self.resize(300, 200)

        self.tree = QTreeWidget()     # 创建树控件
        self.tree.setColumnCount(2)         # 为树控件指定列数
        self.tree.setHeaderLabels(['Key', 'Value'])          # 为树控件指定列标签

        root = QTreeWidgetItem(self.tree)     # 设置根节点
        root.setText(0, 'root')
        root.setText(1, '0')

        # 添加子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, '子节点1')
        child1.setText(1, '子节点1的数据')

        # 添加子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, '子节点2')
        child2.setText(1, '子节点2的数据')

        # 为child2添加一个子节点
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, '子节点2-1')
        child3.setText(1, '子节点2-1的数据')
        self.tree.clicked.connect(self.onTreeClicked)     # 设置单击事件
        self.setCentralWidget(self.tree)    # 将树控件作为中心控件, 即充满整个屏幕

    def onTreeClicked(self, index):
        item = self.tree.currentItem()
        print(range(index.row()))
        print('key = %s, value = %s' % (item.text(0), item.text(1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BasicTreeWidget()
    main.show()
    sys.exit(app.exec_())