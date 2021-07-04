# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:QProcessDemo.py
# @Time:2021/1/10 19:05
# @Author:Jason_Yin


import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication


class Thread(QThread):
    _signal = pyqtSignal(int)  # 定义信号类型为整型

    def __init__(self):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)  # 发射信号


class QProcessDemo(QWidget):
    def __init__(self):
        super(QProcessDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QProgressBar')
        self.resize(300, 300)
        self.vbox = QVBoxLayout()

        self.btn = QPushButton('启动线程')

        self.pbar = QProgressBar(self)

        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)

        self.pbar.setValue(0)
        self.btn.clicked.connect(self.btnFunc)  # 连接槽函数

    def btnFunc(self):
        self.thread = Thread()  # 实例化线程
        self.thread._signal.connect(self.signal_accept)  # 将线程累中定义的信号连接到本类中的信号接收函数中
        self.thread.start()  # 启动线程，启动线程直接调用线程中的start方法，这个方法会调用run函数，所以不用调用run函数
        self.btn.setEnabled(False)

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
            self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QProcessDemo()
    main.show()
    sys.exit(app.exec_())


