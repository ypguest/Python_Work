"""
动态显示当前时间

QTimer
QThread

多线程：用于同时完成多个任务
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ShowTime(QWidget):
    def __init__(self):
        super(ShowTime, self).__init__()
        self.setWindowTitle("动态显示当前时间")

        self.label = QLabel('显示当前时间')
        self.startBtn = QPushButton('开始')
        self.endBtn = QPushButton('结束')

        layout = QGridLayout()  # 通过网格布局，安排控件位置

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)   # 每过多少秒就会触发一个timeout信号

        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.startBtn, 1, 0)
        layout.addWidget(self.endBtn, 1, 1)

        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)

        self.setLayout(layout)

    def showTime(self):   # 刷新当前时间的槽函数
        time = QDateTime.currentDateTime()     # 获取当前时间
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')    # 格式化时间
        self.label.setText(timeDisplay)      # 设置文本

    def startTimer(self):
        self.timer.start(1000)    # 在一定时间间隔内调用一次show time方法, 不断的调用, 以更新时间
        self.startBtn.setEnabled(False)    # 开始后将按钮设置为False
        self.endBtn.setEnabled(True)       # 将结束按钮设置为True

    def endTimer(self):
        self.timer.stop()      # 停止计时
        self.startBtn.setEnabled(True)    # 开始后将按钮设置为False
        self.endBtn.setEnabled(False)       # 将结束按钮设置为True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ShowTime()
    main.show()
    sys.exit(app.exec_())
