"""
计数器空间（QSpinBox）
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QSpinBoxDemo(QWidget):
    def __init__(self):
        super(QSpinBoxDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QSpinBox演示")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.label = QLabel("当前值")  # 设置一个Label
        self.label.setAlignment(Qt.AlignCenter)  # 将Label设置居中位置
        layout.addWidget(self.label)

        self.sb = QSpinBox()      # 设置一个QSpinBox
        layout.addWidget(self.sb)
        self.sb.valueChanged.connect(self.ValueChange)
        self.setLayout(layout)

    def ValueChange(self):
        self.label.setText('当前值:' + str(self.sb.value()))   # 使Label上的信息进行改变的槽


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QSpinBoxDemo()
    main.show()
    sys.exit(app.exec_())
