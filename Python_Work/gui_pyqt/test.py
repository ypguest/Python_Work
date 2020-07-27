from PyQt5.QtSql import *

print(QSqlDatabase.drivers())
db = QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("localhost")
db.setPort(3306)
db.setUserName("root")
db.setPassword("yp*963.")
db.setDatabaseName("testdb")





