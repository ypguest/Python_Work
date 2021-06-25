"""
生成主Widget
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from MainLayout2 import FamilyQuery, ProdQuery, FunButton, TextQuery
from MainLayout3 import WipTable


class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self.SetScreen()  # 设置窗口大小
        self.setFont(QFont("等线", 12))   # 设置字体及大小

        # -------------画分割线-------------
        self.mainline1 = QFrame(self)
        self.mainline1.setGeometry(QRect(0, 0, 300, self.height()))    # QRect(起始的x坐标，起始的y坐标，宽度，高度)
        self.mainline1.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.mainline2 = QFrame(self)
        self.mainline2.setGeometry(QRect(300, 0, self.width()-300, 230))
        self.mainline2.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.mainline3 = QFrame(self)
        self.mainline3.setGeometry(QRect(300, 230, self.width()-300, self.height()-230))
        self.mainline3.setFrameStyle(QFrame.Box | QFrame.Sunken)

        # -------------设置mainlayout1的树控件-------------
        mainlayout1 = QHBoxLayout()
        self.tree = QTreeWidget()     # 创建树控件
        self.tree.setColumnCount(1)         # 为树控件指定列数

        self.tree.setHeaderHidden(True)
        root1 = QTreeWidgetItem(self.tree)      # 设置根节点
        root1.setText(0, 'WIP')

        child1 = QTreeWidgetItem(root1)         # 添加子节点1
        child1.setText(0, 'Wafer WIP')

        child2 = QTreeWidgetItem(root1)         # 添加子节点2
        child2.setText(0, 'Component WIP')

        child3 = QTreeWidgetItem(root1)         # 添加子节点3
        child3.setText(0, 'System WIP')

        mainlayout1.addWidget(self.tree)
        self.mainline1.setLayout(mainlayout1)

        # -------------添加mainlayout2的Qeuery控件-------------
        mainlayout2 = QHBoxLayout()
        self.ProdQuery1 = FamilyQuery()

        self.ProdQuery2 = ProdQuery()
        self.ProdQuery3 = FunButton()
        self.ProdQuery4 = TextQuery()

        spacerItem1 = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)  # 增加横向弹簧线

        mainlayout2.addWidget(self.ProdQuery1)
        mainlayout2.addWidget(self.ProdQuery2)
        mainlayout2.addWidget(self.ProdQuery3)
        mainlayout2.addItem(spacerItem1)
        mainlayout2.addWidget(self.ProdQuery4)

        self.mainline2.setLayout(mainlayout2)

        # -------------添加mainlayout3的数据控件-------------
        mainlayout3 = QHBoxLayout()
        self.tableWidget = WipTable()
        mainlayout3.addWidget(self.tableWidget)
        self.mainline3.setLayout(mainlayout3)

        # ------------模块间的通讯--------------------------
        self.ProdQuery1.sendToProQuery.connect(self.ProdQuery2.getMsg)   # 将ProdNickQuery()中选取的Nick Name与ProdQuery()进行绑定

        self.ProdQuery3.sendToMainL3.connect(self.tableWidget.iniLocal)    # 单击任何ProdQuery的push button均会将MainLayout3内部参数初始化

        self.ProdQuery3.sendToMainL3.connect(self.ProdQuery1.sendMsg)      # 功能按钮被单击，触发ProdQuery1的sendMsg函数
        self.ProdQuery3.sendToMainL3.connect(self.ProdQuery2.sendMsg)      # 功能按钮被单击，触发ProdQuery2的sendMsg函数

        self.ProdQuery1.sendToMain.connect(self.tableWidget.getQue1Msg)   # 触发sendMeg函数后，将ProdQuery1中的productFam信息传递给MainLayout3中的getQue1Msg函数
        self.ProdQuery2.sendToMainL3.connect(self.tableWidget.getQue2Msg)   # 触发sendMeg函数后，将ProdQuery2中的fab,prod,Ver信息传递给MainLayout3中的getQue2Msg函数
        self.ProdQuery3.sendToMainL3.connect(self.tableWidget.getFunMsg)   # 触发sendMeg函数后，将ProdQuery3中的sendToMainL3信息传递给MainLayout3中的getFunMsg函数

    def SetScreen(self):
        """ 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi """
        screen = QApplication.desktop().screenGeometry()  # 获取屏幕的分辨率
        width = int(screen.width())
        height = int(screen.height() * 0.9)
        self.setGeometry(0, int(screen.height() * 0.05), width, height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec_())
