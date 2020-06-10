"""
动态添加，修改和删除树控件中的节点

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ModifyTree(QWidget):
    def __init__(self):
        super(ModifyTree, self).__init__()
        self.setWindowTitle("TreeWidget例子")

        operationLayout = QHBoxLayout()
        addBtn = QPushButton('添加节点')
        updateBtn = QPushButton('更新节点')
        deleteBtn = QPushButton('删除节点')

        # 将button加入的operationLayout
        operationLayout.addWidget(addBtn)
        operationLayout.addWidget(updateBtn)
        operationLayout.addWidget(deleteBtn)

        addBtn.clicked.connect(self.addNode)
        updateBtn.clicked.connect(self.updateNode)
        deleteBtn.clicked.connect(self.deleteNode)

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

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(operationLayout)
        mainLayout.addWidget(self.tree)
        self.setLayout(mainLayout)

    def onTreeClicked(self, index):
        item = self.tree.currentItem()
        print(range(index.row()))
        print('key = %s, value = %s' % (item.text(0), item.text(1)))

    # 添加节点
    def addNode(self):
        item = self.tree.currentItem()  # 获得当前节点
        node = QTreeWidgetItem(item)
        node.setText(0, '新节点')
        node.setText(1, '新数据')

    # 修改节点
    def updateNode(self):
        item = self.tree.currentItem()  # 获得当前节点
        item.setText(0, '修改节点')
        item.setText(1, '数据已修改')

    def deleteNode(self):
        item = self.tree.currentItem()  # 获得当前节点
        root = self.tree.invisibleRootItem()    # 使root的父节点可见
        for item in self.tree.selectedItems():
            (item.parent() or root).removeChild(item)    # item.parent() 和root中只要有一个不为空, 就不出错


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ModifyTree()
    main.show()
    sys.exit(app.exec_())