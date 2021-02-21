# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:QPainter.py
# @Time:2021/1/2 15:38
# @Author:Jason_Yin

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class Drawing(QWidget):
    def __init__(self):
        super(Drawing, self).__init__()
        self.setWindowTitle("在窗口中绘制文字")
        self.resize(300, 200)
        self.text = "欢迎学习 PyQt5"

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawText(event, painter)
        painter.end()

    def drawText(self, event, gp):
        gp.setPen(QColor(168, 34, 3))
        gp.setFont(QFont("SimSun", 20))
        gp.drawText(event.rect(), Qt.AlignCenter, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Drawing()
    main.show()
    sys.exit(app.exec_())

