"""
对话框: QDialog
1. QMessageBox
2. QColorDialog
3. QFileDialog
4. QFontDialog
5. QInputDialog

窗口
QMainWindow
QWidget
QDialog
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QDialogDemo(QMainWindow):
    def __init__(self):
        super(QDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QDialog案例')
        self.resize(300, 200)

        self.button = QPushButton(self)     # 在mainwindow中使用Pushbutton
        self.button.setText('弹出对话框')
        self.button.move(50, 50)      # 将button移动到窗口50,50位置
        self.button.clicked.connect(self.showDialog)

    def showDialog(self):
        dialog = QDialog()
        button = QPushButton('确定', dialog)
        button.clicked.connect(dialog.close)
        button.move(50, 50)
        dialog.setWindowTitle('对话框')
        dialog.setWindowModality(Qt.ApplicationModal)   # 设置对话框以模式方式显示，则mainWindow无法激活
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialogDemo()
    main.show()
    sys.exit(app.exec_())



