# ///////////////////////////////////////////////////////////////
#
# BY: Jason.Yin
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ui_main import Ui_Form


class CustomGrip(QWidget):
    def __init__(self):
        super(CustomGrip, self).__init__()
        u = Ui_Form()
        u.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = CustomGrip()
    main.show()
    sys.exit(app.exec())
