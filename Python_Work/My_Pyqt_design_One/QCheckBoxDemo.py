"""
按钮控件（QPushButton）

QAbstractButton  # 所有按钮的父类

子类按钮
1. QPushButton      # 常规按钮
2. AToolButton      # 工具条按钮
3. QRadioButton     # 单选按钮
4. QCheckBox        # 复选按钮    V

复选按钮，3中状态
未选中： 0
半选中： 1
选中: 2

"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QRadioButtonDemo(QWidget):
    def __init__(self):
        super(QRadioButtonDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('复选框控件演示')
        layout = QHBoxLayout()

        groupBox = QGroupBox("CheckBoxes")
        groupBox.setFlat(True)

        self.checkBox1 = QCheckBox('复选框控件1')
        self.checkBox1.setChecked(True)           # 是复选框处于被选中状态，该方法只能设置两种状态
        self.checkBox1.stateChanged.connect(lambda: self.checkboxState(self.checkBox1))
        layout.addWidget(self.checkBox1)

        self.checkBox2 = QCheckBox('复选框控件2')
        self.checkBox2.stateChanged.connect(lambda: self.checkboxState(self.checkBox2))
        layout.addWidget(self.checkBox2)

        self.checkBox3 = QCheckBox('复选框控件3')   # 设置半选中
        self.checkBox3.setTristate(True)          # 设置复选框可用于半选中状态
        self.checkBox3.setCheckState(Qt.PartiallyChecked)   # 设置当前的状态为半选中状态
        self.checkBox3.stateChanged.connect(lambda: self.checkboxState(self.checkBox3))
        layout.addWidget(self.checkBox3)

        groupBox.setLayout(layout)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)

        self.setLayout(mainLayout)

    def checkboxState(self, cb):
        check1Status = self.checkBox1.text() + ', isChecked=' + str(self.checkBox1.isChecked()) + ',checkState=' + str(self.checkBox1.checkState()) + '\n'
        check2Status = self.checkBox2.text() + ', isChecked=' + str(self.checkBox2.isChecked()) + ',checkState=' + str(self.checkBox2.checkState()) + '\n'
        check3Status = self.checkBox3.text() + ', isChecked=' + str(self.checkBox3.isChecked()) + ',checkState=' + str(self.checkBox3.checkState()) + '\n'
        print(check1Status + check2Status + check3Status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QRadioButtonDemo()
    main.show()
    sys.exit(app.exec_())
