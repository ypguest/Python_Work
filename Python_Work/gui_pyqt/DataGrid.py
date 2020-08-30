
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Python_Work.gui_pyqt.mysqlconfig import MySQL


class DataGrid(QWidget):
    def __init__(self):
        super(DataGrid, self).__init__()
        self.setWindowTitle('分页查询')

        operatorLayout = QHBoxLayout()

        # 当前页
        self.currentPage = 0

        # 总页数
        self.totalPage = 0

        # 总记录数
        self.totalRecordCoutn = 0

        # 每页显示记录数
        self.pageRecordCount = 100

        # 当前页信息
        self.switchPage = QLabel("当前%s/%s页" % (self.currentPage, self.totalPage))

        # 前一页按钮
        self.prevButton = QPushButton("前一页")

        # 后一页按钮
        self.nextButton = QPushButton("后一页")

        operatorLayout.addWidget(QSplitter())
        operatorLayout.addWidget(self.switchPage)
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)

        self.setLayout(operatorLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataGrid()
    main.show()
    sys.exit(app.exec_())




