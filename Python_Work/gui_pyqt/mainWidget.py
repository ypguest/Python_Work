"""
生成主Widget
"""

import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Python_Work.gui_pyqt.ProdQuery import ProdNickQuery, ProdQuery


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.SetScreen()  # 设置窗口大小
        self.iniUI()

        # -------画分割线-------
        self.Hline = QFrame(self)
        self.Hline.setGeometry(QRect(300, 220, self.width()-220, 20))
        self.Hline.setFrameShape(QFrame.HLine)
        self.Hline.setFrameShadow(QFrame.Sunken)
        self.Vline = QFrame(self)
        self.Vline.setGeometry(QRect(200, 0, 200, self.height()))
        self.Vline.setFrameShape(QFrame.VLine)
        self.Vline.setFrameShadow(QFrame.Sunken)

    def iniUI(self):
        layout = QHBoxLayout()

        ProdQuery1 = ProdNickQuery()
        prodQuery2 = ProdQuery()

        # todo 增加lot 查询界面
        layoutQuery = QVBoxLayout()
        lineEdit = QLineEdit("Lot ID")
        QueryButton = QPushButton("Query")
        CancelButton = QPushButton("Cancel")

        layoutQuery.addWidget(lineEdit)
        layoutQuery.addWidget(QueryButton)
        layoutQuery.addWidget(CancelButton)

        spacerItem = QSpacerItem(200, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)  # 增加横向弹簧线

        # todo 增加Function界面
        layoutFun = QVBoxLayout()
        lineEditFun = QPushButton("New WIP")
        allWipButton = QPushButton("All WIP")
        holdTButton = QPushButton("Hold Time")
        commButton = QPushButton("Comment Update")
        spacerFunTop = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)  # 增加竖向弹簧线
        spacerFunBot = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)  # 增加竖向弹簧线

        layoutFun.addItem(spacerFunTop)
        layoutFun.addWidget(lineEditFun)
        layoutFun.addWidget(allWipButton)
        layoutFun.addWidget(holdTButton)
        layoutFun.addWidget(commButton)
        layoutFun.addItem(spacerFunBot)

        layout.addWidget(ProdQuery1)
        layout.addWidget(prodQuery2)
        layout.addItem(layoutQuery)
        layout.addItem(spacerItem)
        layout.addItem(layoutFun)

        self.setLayout(layout)

        ProdQuery1.sendmsg.connect(prodQuery2.getmsg)  # 将ProdNickQuery()中选取的Nick Name与ProdQuery()进行绑定

    def SetScreen(self):  # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        screen = QApplication.desktop().screenGeometry()  # 获取屏幕的分辨率
        width = int(screen.width() * 0.9)
        height = int(screen.height() * 0.9)
        self.setGeometry(int(screen.width() * 0.05), int(screen.height() * 0.05), width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec_())
