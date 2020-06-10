#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mainWindows(QMainWindow):
    def __init__(self):
        super(mainWindows,self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("my gui")
        self.resize(600, 600)
        toolbar = self.addToolBar(u'退出')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = mainWindows()
    main.show()
    sys.exit(app.exec_())