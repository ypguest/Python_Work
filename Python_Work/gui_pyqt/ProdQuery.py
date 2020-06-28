"""
生成Product查询的ListView, 给出Nick Name
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql


class MainWindows(QWidget):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("UniIC颗粒查询系统")
        self.SetScreen()   # 设置窗口大小

        layout = QVBoxLayout()

        ProdQuery1 = ProdNickQuery()
        prodQuery2 = ProdQuery()

        layout.addWidget(ProdQuery1)
        layout.addWidget(prodQuery2)

        self.setLayout(layout)

    def SetScreen(self):  # 获取屏幕的分辨率, 并将窗体的大小设定为屏幕-100 pi
        screen = QApplication.desktop().screenGeometry()   # 获取屏幕的分辨率
        width = int(screen.width() * 0.9)
        height = int(screen.height() * 0.9)
        self.setGeometry(int(screen.width() * 0.05), int(screen.height()*0.05), width, height)


# todo 生成Product查询的ListView, 给出Nick Name
class ProdNickQuery(QWidget):
    def __init__(self):
        super(ProdNickQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product Nick Name Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 总体垂直布局

        self.listview = QListView()
        listModel = QStringListModel()           # 创建封装列表数据源的模型
        self.list = ProdList("Nick_Name")     # 创建数据源
        listModel.setStringList(self.list)       # 将数据和模型进行关联
        self.listview.setModel(listModel)             # 模型与空间关联
        self.listview.clicked.connect(self.clicked)
        layout.addWidget(self.listview, 1, 0, 3, 4)               # 将控件放入栅格布局，起始行，列，跨越行，列
        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Nick Name")
        self.Button1 = QPushButton("OK")
        self.Button1.setFixedWidth(35)
        layout.addWidget(self.lineEdit, 5, 0, 1, 3)
        layout.addWidget(self.Button1, 5, 3, 1, 1)

        self.groupbox.setLayout(layout)

    def clicked(self, qModelIndex):  # 点击后将值输入到LineEdit内
        self.lineEdit.setText(self.list[qModelIndex.row()])


# todo 生成Product_ID与Product_Version的联和查询
class ProdQuery(QWidget):
    def __init__(self):
        super(ProdQuery, self).__init__()
        self.setFixedSize(300, 200)

        self.groupbox = QGroupBox('Product and Version Select', self)   # 增加GroupBox框体
        self.groupbox.setFixedSize(300, 200)  # 设置控件的大小
        self.groupbox.setAlignment(Qt.AlignLeft)    # 将QGroup的名称放到左边

        layout = QGridLayout()                    # 设置栅格布局

        self.listviewPid = QListView()
        self.listModelPid = QStringListModel()           # 创建封装列表数据源的模型
        self.listPid = ProdList("UniIC_Product_ID")     # 通过数据库查询Product_ID, 并根据结果创建数据源

        self.listModelPid.setStringList(self.listPid)       # 将数据和模型进行关联
        self.listviewPid.setModel(self.listModelPid)             # 模型与控件关联
        self.listviewPid.clicked.connect(self.clickedPid)        # 当数据进行切换时，将选中的数据放入LineEdit中

        self.listviewVer = QListView()
        self.listModeVer = QStringListModel()           # 创建封装列表数据源的模型
        self.listVer = ProdList("UniIC_Product_Version")     # 创建数据源
        self.listModeVer.setStringList(self.listVer)       # 将数据和模型进行关联
        self.listviewVer.setModel(self.listModeVer)             # 模型与空间关联
        self.listviewVer.clicked.connect(self.clickedVer)

        self.lineEdit = QLineEdit("")      # 确认的信息显示到Label中
        self.lineEdit.setPlaceholderText("Please Select Product ID & Ver")
        self.Button1 = QPushButton("OK")
        self.Button1.setFixedWidth(35)

        # todo 设置所有控件布局
        layout.addWidget(self.listviewPid, 0, 0, 1, 1)  # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.listviewVer, 0, 2, 1, 1)               # 将控件放入栅格布局，起始行，列，跨越行，列
        layout.addWidget(self.lineEdit, 1, 0, 1, 3)
        layout.addWidget(self.Button1, 1, 3, 1, 1)

        self.groupbox.setLayout(layout)

    def clickedPid(self, qModelIndex):
        self.lineEdit.setText(self.listPid[qModelIndex.row()])      # 将LineEdit里的内容进行写入
        self.listviewVer = ProdQueryList(self.listPid[qModelIndex.row()])     # 创建数据源
        self.listModeVer.setStringList(self.listviewVer)  # 将数据和模型进行关联

    def clickedVer(self, qModelIndex):
        if self.lineEdit.text() is None:
            self.lineEdit.setText(self.listviewVer[qModelIndex.row()])
        elif len(self.lineEdit.text().split(",")) < 2:
            self.lineEdit.setText(self.lineEdit.text() + ',' + self.listviewVer[qModelIndex.row()])
        else:
            self.lineEdit.setText(self.lineEdit.text().split(",")[0] + ',' + self.listviewVer[qModelIndex.row()])


# todo 用于class ProdQuery中, 用于给出关键字Item，并查找psmc_product_version表中所以的匹配值
def ProdList(item):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE configdb;')
            cursor.execute('SELECT distinct %s FROM psmc_product_version' % item)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


# todo 用于Class ProdQuery中, 用于给定UniIC_Product_Id，查找出对应的所有UniIC_Product_Version
def ProdQueryList(arg):
    sql_config = {
        'user': 'root',
        'password': 'yp*963.',
        'host': 'localhost',
        'database': 'testdb',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**sql_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute('USE configdb;')
            cursor.execute("SELECT distinct UniIC_Product_Version FROM psmc_product_version WHERE UniIC_Product_Id = '%s'" % arg)
            result = cursor.fetchall()
    finally:
        connection.close()
    return [result[i][0] for i in range(len(result))]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindows()
    main.show()
    sys.exit(app.exec_())
