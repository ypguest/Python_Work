#!/usr/bin/evn python3


# !/usr/bin/evn python3

import sys
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QApplication, QTreeView

class Model(QAbstractItemModel):

    def columnCount(self, parent):
        return 4

    def rowCount(self, parent):
        return 2

    def data(self, index, role):
        return 1,2


app = QApplication(sys.argv)

model = Model()
list_view = QTreeView()
list_view.setModel(model)
list_view.show()

app.exec_()
