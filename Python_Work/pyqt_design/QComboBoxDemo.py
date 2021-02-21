import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ComboBoxDemo(QWidget):
    def __init__(self):
        super(ComboBoxDemo, self).__init__()
        self.initUI()

    QAbstractItemView
    def initUI(self):
        self.setWindowTitle("Combo 例子")
        self.resize(300, 90)
        layout = QVBoxLayout()
        self.Label1 = QLabel("")
        layout.addWidget(self.Label1)

        self.ComboBox1 = QComboBox()
        self.ComboBox1.addItems(["Java", "C+", "Python"])
        self.ComboBox1.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.ComboBox1)

        self.setLayout(layout)

    def selectionchange(self, i):
        self.Label1.setText(self.ComboBox1.currentText())
        print('items in the list are:')
        for count in range(self.ComboBox1.count()):
            print("Item" + str(count) + "=" + self.ComboBox1.itemText(count))
            print("Current index", i, "selection changed", self.ComboBox1.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ComboBoxDemo()
    main.show()
    sys.exit(app.exec_())


