from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

db = QSqlDatabase.addDatabase("QODBC")
db.setHostName("192.168.55.110")
db.setPort(3306)
db.setUserName("root")
db.setPassword("yp*963.")
print(db.open())
