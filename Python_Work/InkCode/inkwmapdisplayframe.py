# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Dialog(QWidget):
    def __init__(self):
        super(Ui_Dialog, self).__init__()

        self.layoutWidget = None
        self.horizontalLayout = None
        self.verticalLayout = None
        self.horizontalLayout_2 = None

        self.pushReadFileName = None

        self.comboBoxIddNames = None
        self.comboBoxFcNames = None
        self.pushButtonAddBinInk = None
        self.pushButtonAddFcInk = None
        self.pushButtonAddIddInk = None
        self.pushButtonSetColor = None
        self.pushButtonResetTable = None
        self.pushButtonExportWmap = None
        self.comboBoxRingNum = None
        self.tableWidget = None
        self.labelInfo = None

        self.label = None
        self.label_1 = None
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None
        self.label_5 = None
        self.label_6 = None

        self.setupUi()

    def setupUi(self):

        self.setWindowTitle("Ink System")
        self.setObjectName("layoutWidget")
        self.setGeometry(QRect(0, 10, 1151, 541))

        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # ---- pushReadFileName 设置 ----
        self.pushReadFileName = QPushButton()
        self.pushReadFileName.setObjectName("pushReadFileName")

        self.verticalLayout.addWidget(self.pushReadFileName)

        # ---- label_1 设置 ----
        self.label_1 = QLabel()
        font = QFont()
        font.setPointSize(5)
        self.label_1.setFont(font)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.verticalLayout.addWidget(self.label_1)

        # ---- pushButtonAddBinInk 设置 ----
        self.pushButtonAddBinInk = QPushButton()
        self.pushButtonAddBinInk.setObjectName("pushButtonAddBinInk")
        self.verticalLayout.addWidget(self.pushButtonAddBinInk)

        # ---- label_2 设置 ----
        self.label_2 = QLabel()
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        # ---- label_4 设置 ----
        self.label_4 = QLabel()
        font = QFont()
        font.setPointSize(5)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        # ---- comboBoxFcNames 设置 ----
        self.comboBoxFcNames = QComboBox()
        self.comboBoxFcNames.setObjectName("comboBoxFcNames")
        self.verticalLayout.addWidget(self.comboBoxFcNames)

        # ---- pushButtonAddFcInk 设置 ----
        self.pushButtonAddFcInk = QPushButton()
        self.pushButtonAddFcInk.setObjectName("pushButtonAddFcInk")
        self.verticalLayout.addWidget(self.pushButtonAddFcInk)

        # ---- label_5 设置 ----
        self.label_5 = QLabel()
        font = QFont()
        font.setPointSize(5)
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)

        # ---- label_3 设置 ----
        self.label_3 = QLabel()
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        # ---- comboBoxIddNames 设置 ----
        self.comboBoxIddNames = QComboBox()
        self.comboBoxIddNames.setObjectName("comboBoxIddNames")
        self.verticalLayout.addWidget(self.comboBoxIddNames)

        # ---- pushButtonAddIddInk 设置 ----
        self.pushButtonAddIddInk = QPushButton()
        self.pushButtonAddIddInk.setObjectName("pushButtonAddIddInk")
        self.verticalLayout.addWidget(self.pushButtonAddIddInk)

        # ---- label_6 设置 ----
        self.label_6 = QLabel()
        font = QFont()
        font.setPointSize(5)
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)

        # ---- pushButtonSetColor 设置 ----
        self.pushButtonSetColor = QPushButton()
        self.pushButtonSetColor.setObjectName("pushButtonSetColor")
        self.verticalLayout.addWidget(self.pushButtonSetColor)

        # ---- pushButtonResetTable 设置 ----
        self.pushButtonResetTable = QPushButton()
        self.pushButtonResetTable.setObjectName("pushButtonResetTable")
        self.verticalLayout.addWidget(self.pushButtonResetTable)

        # ---- pushButtonExportWmap 设置 ----
        self.pushButtonExportWmap = QPushButton()
        self.pushButtonExportWmap.setObjectName("pushButtonExportWmap")
        self.verticalLayout.addWidget(self.pushButtonExportWmap)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(spacerItem)

        # ---- 设置模块2 ----
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label = QLabel()
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        self.comboBoxRingNum = QComboBox()
        self.comboBoxRingNum.setObjectName("comboBoxRingNum")
        self.comboBoxRingNum.addItem("")
        self.comboBoxRingNum.addItem("")
        self.comboBoxRingNum.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBoxRingNum)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.labelInfo = QLabel()
        self.labelInfo.setGeometry(QRect(80, 560, 1071, 20))
        self.labelInfo.setText("")
        self.labelInfo.setObjectName("labelInfo")

        self.setLayout(self.horizontalLayout)

        self.retranslateUi()
        # QMetaObject.connectSlotsByName()

    def retranslateUi(self):
        self.pushReadFileName.setText("Select File")
        self.label_1.setText("+++++++++++++++++")
        self.pushButtonAddBinInk.setText("By Bin Ink")
        self.label_2.setText("FRC Name:")
        self.label_4.setText("+++++++++++++++++")

        self.pushButtonAddFcInk.setText("By FRC Ink")
        self.label_5.setText("+++++++++++++++++")
        self.label_3.setText("IDD Name:")
        self.pushButtonAddIddInk.setText("By Idd Ink")
        self.label_6.setText("+++++++++++++++++")
        self.pushButtonSetColor.setText("Fill Color")
        self.pushButtonResetTable.setText("Reset Table")
        self.pushButtonExportWmap.setText("Export WMap")
        self.label.setText("Ring:")
        self.comboBoxRingNum.setItemText(0, "1")
        self.comboBoxRingNum.setItemText(1, "2")
        self.comboBoxRingNum.setItemText(2, "3")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Ui_Dialog()
    main.show()
    sys.exit(app.exec_())