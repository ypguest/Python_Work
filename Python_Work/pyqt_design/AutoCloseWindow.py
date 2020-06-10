"""
让程序定时关闭
QTimer.singleShot 在指定时间以后只调用一次代码

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = QLabel('<font color =red size =140><b>Hello World, 窗口在5秒后自动关闭！</b></font>')
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)   # 设置窗口的闪屏, 无框架
    label.show()
    QTimer.singleShot(5000, app.quit)   # 设置在一段时间只执行一次
    sys.exit(app.exec_())
