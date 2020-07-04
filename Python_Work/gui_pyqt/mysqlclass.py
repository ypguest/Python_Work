# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
设置sql操作相关的类，涉及到
"""
import MySQLdb


class MySQL(object):
    def __init__(self, host='localhost', user="root", password="yp*963.", port=3306, charset="utf8"):
        """实例化后自动连接至数据库"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.cur = None
        self.con = None    # 指针
        # connect to mysql
        try:
            self.con = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
            self.con.autocommit(False)
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase connect error,please check the sql config.")

    def close(self):
        self.cur.close()
        self.con.close()

    def selectDb(self, db):
        """选择数据库"""
        try:
            self.cur.execute('USE {};'.format(db))
        except:
            raise Exception("db error,please check the sql config.")

    def fetchRow(self, sql_str, params=()):
        """根据sql语句查询数据库，返回一行结果"""
        try:
            self.cur.execute(sql_str, params)
            result = self.cur.fetchone()
            self.close()
        except:
            raise Exception("fetchRow Error, please check sql description")
        return result

    def fetchAll(self, sql_str, params=()):
        """根据sql语句查询数据库，返回所有结果"""
        try:
            self.cur.execute(sql_str, params)
            result = self.cur.fetchall()
            desc = self.cur.description
            self.close()
        except:
            raise Exception("fetchRow Error, please check sql description")
        return result, desc
    #
    # def insert(self, table_name, data):
    #     columns = data.keys()
    #     _prefix = "".join(['INSERT INTO `', table_name, '`'])
    #     _fields = ",".join(["".join(['`', column, '`']) for column in columns])
    #     _values = ",".join(["%s" for i in range(len(columns))])
    #     _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
    #     _params = [data[key] for key in columns]
    #     return self.cur.execute(_sql, tuple(_params))

    # def update(self, tbname, data, condition):
    #     _fields = []
    #     _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
    #     for key in data.keys():
    #         _fields.append("%s = %s" % (key, data[key]))
    #     _sql = "".join([_prefix, _fields, "WHERE", condition])
    #
    #     return self.cur.execute(_sql)
    #
    # def delete(self, tbname, condition):
    #     _prefix = "".join(['DELETE FROM  `', tbname, '`', 'WHERE'])
    #     _sql = "".join([_prefix, condition])
    #     return self.cur.execute(_sql)
    #
    # def getLastInsertId(self):
    #     return self.cur.lastrowid
    #
    # def rowcount(self):
    #     return self.cur.rowcount
    #
    # def commit(self):
    #     self.conn.commit()
    #
    # def rollback(self):
    #     self.conn.rollback()
    #



if __name__ == '__main__':
    mysql = MySQL()
    mysql.selectDb('testdb')
    tbname = 'psmc_lot_tracing_table'
    sql = 'SELECT Lot_ID from {}'.format(tbname)
    print(mysql.fetchAll(sql))



