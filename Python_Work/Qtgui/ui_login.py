# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QWidget(self)
        self.widget.setGeometry(QRect(30, 20, 341, 102))
        self.widget.setObjectName("widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.label_3.setBuddy(self.comboBox)
        self.label.setBuddy(self.lineEdit)
        self.label_2.setBuddy(self.lineEdit_2)
        self.label_4.setBuddy(self.lineEdit_3)

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "dbType:"))
        self.label.setText(_translate("Dialog", "user:"))
        self.label_2.setText(_translate("Dialog", "database:"))
        self.label_4.setText(_translate("Dialog", "password:"))
        self.comboBox.setItemText(0, _translate("Dialog", "Local"))
        self.comboBox.setItemText(1, _translate("Dialog", "Server"))
        self.lineEdit.setText(_translate("Dialog", "root"))
        self.lineEdit_2.setText(_translate("Dialog", "testdb"))
        self.lineEdit_3.setText(_translate("Dialog", "yp*963."))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Ui_Dialog()
    main.show()
    sys.exit(app.exec_())
