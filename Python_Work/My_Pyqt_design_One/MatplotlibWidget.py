import sys
import random

import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolBar
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终父类其实是QWidget"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 设置中文显示
        plt.rcParams['font.family'] = ['SimHei']    # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示符合

        # 新建一个绘图对象
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 建立一个字图，如果要建立复合图，可以在这里修改
        self.axes = self.fig.add_subplot(111)

        # self.axes.hold(False)  # 每次绘图时都不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def start_static_plot(self):
        self.fig.suptitle("测试静态图")
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('静态图：Y轴')
        self.axes.set_xlabel('静态图：X轴')
        self.axes.grid(True)

    def start_dynamic_plot(self, *args, **kwargs):

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)  # 触发的时间间隔为1秒

    def update_figure(self):
        self.fig.suptitle("测试动态图")
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_ylabel('动态图：Y轴')
        self.axes.set_xlabel('动态图：X轴')
        self.axex.grid(True)
        self.draw()


class MatplotlibWidget(QWidget):
    def __init__(self):
        super(MatplotlibWidget, self).__init__()
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        # self.mpl.start_static_plot()   # 如果想要在初始化是就呈现静态图，请取消这行注释
        self.mpl.start_dynamic_plot()    # 如果想要在初始化是就呈现动态图，请取消这行注释
        self.mpl_ntb = NavigationToolBar(self.mpl, self)    # 添加完整的工具栏
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    # ui.mpl.start_static_plot()   # 测试静态图效果
    ui.mpl.start_dynamic_plot()   # 测试动态图效果
    ui.show()
    sys.exit(app.exec_())

