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
        self.setWindowTitle("树控件(QTreeWidget)的基本用法")

        self.tree = QTreeWidget()     # 创建树控件
        self.tree.setColumnCount(2)         # 为树控件指定列数

        # 指定列标签
        self.tree.setHeaderLabels(['Key', 'Value'])

        root = QTreeWidgetItem(self.tree)     # 设置根节点
        root.setText(0, '根节点')
        root.setIcon(0, QIcon('./images/Bird.ico'))

        # 设置行间距
        self.tree.setColumnWidth(0, 160)

        # 添加子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, '子节点1')
        child1.setIcon(0, QIcon('./images/Bird.ico'))
        child1.setText(1, '子节点1的数据')
        child1.setCheckState(0, Qt.Checked)

        # 添加子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, '子节点2')
        child2.setIcon(0, QIcon('./images/Bird.ico'))

        # 为child2添加一个子节点
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, '子节点2-1')
        child3.setText(1, '子节点2-1的数据')
        child3.setIcon(0, QIcon('./images/Bird.ico'))

        self.tree.expandAll()    # 展开所有的节点

        self.setCentralWidget(self.tree)    # 将树控件作为中心控件, 即充满整个屏幕


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BasicTreeWidget()
    main.show()
    sys.exit(app.exec_())