"""
显示列表数据（QListView）
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QListViewDemo(QWidget):
    def __init__(self):
        super(QListViewDemo, self).__init__()
        self.setWindowTitle('QListView案例')
        self.resize(300, 270)
        layout = QVBoxLayout()

        listview = QListView()
        listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = ["列表项1", '列表项2', '列表项3']     # 创建数据源

        listModel.setStringList(self.list)       # 将数据和模型进行他关联
        listview.setModel(listModel)             # 模型与空间关联
        listview.clicked.connect(self.clicked)

        layout.addWidget(listview)               # 将控件放入垂直布局

        self.setLayout(layout)

    def clicked(self, item):
        QMessageBox.information(self, "QListView", "您选择了：" + self.list[item.row()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QListViewDemo()
    main.show()
    sys.exit(app.exec_())