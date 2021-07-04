"""
扩展的列表控件（QListWidget）
"""


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QListWidgetDemo(QMainWindow):
    def __init__(self):
        super(QListWidgetDemo, self).__init__()
        self.setWindowTitle('QListWidget案例')
        self.resize(300, 270)
        self.listwidget = QListWidget()

        self.listwidget.addItem('item1')
        self.listwidget.addItem('item2')
        self.listwidget.addItem('item3')
        self.listwidget.addItem('item4')
        self.listwidget.addItem('item5')

        self.listwidget.itemClicked.connect(self.clicked)

        self.setCentralWidget(self.listwidget)

    def clicked(self, Index):
        QMessageBox.information(self, "QListView", "您选择了：" + self.listwidget.item(self.listwidget.row(Index)).text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QListWidgetDemo()
    main.show()
    sys.exit(app.exec_())