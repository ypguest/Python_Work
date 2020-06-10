"""
绘图API: 绘制文本
1. 文本
2. 各种图像(直线，点，椭圆，弧，扇形，多边形)
3. 图像

QPainter
painter = QPainter()
painter.begin()
paiter.drawText(...)
paiter.end

必须在painterEvent事件方法中绘制各种元素

"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DrawTextDemo(QWidget):
    def __init__(self):
        super(DrawTextDemo, self).__init__()
        self.setWindowTitle('在窗口上绘制文本')
        self.resize(300, 200)
        self.text = 'Python从菜鸟到高手'

    def paintEvent(self, QPaintEvent):
        painter =QPainter(self)
        painter.begin(self)

        painter.setPen(QColor(154, 542, 568))
        painter.setFont(QFont('Arial', 25))

        painter.drawText(QPaintEvent.rect(), Qt.AlignCenter, self.text)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawTextDemo()
    main.show()
    sys.exit(app.exec_())
