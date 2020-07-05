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
        self.conn = None    # 指针
        # connect to mysql
        try:
            self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
            self.conn.autocommit(False)
            self.cur = self.conn.cursor()
        except:
            raise Exception("DataBase connect error,please check the sql config.")

    def close(self):
        """关闭数据库"""
        self.cur.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def selectDb(self, db):
        """选择数据库"""
        try:
            self.cur.execute('USE {};'.format(db))
        except:
            raise Exception("db error,please check the sql config.")

    def fetchRow(self, sql_str, params=()):
        """根据sql语句查询数据库，返回一行结果，并关闭数据库"""
        try:
            self.cur.execute(sql_str, params)
            _result = self.cur.fetchone()
            _desc = self.cur.description
            self.close()
            _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
            _result = list(_result)
        except:
            raise Exception("fetchRow Error, please check sql description")
        return _desc, _result

    def fetchAll(self, sql_str, params=()):
        """根据sql语句查询数据库，返回所有结果，并关闭数据库（表头及数据以list形式返回）"""
        try:
            self.cur.execute(sql_str, params)
            _result = self.cur.fetchall()
            _desc = self.cur.description           # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
            self.close()
            _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
            _result = [list(i) for i in _result]
        except:
            raise Exception("fetchRow Error, pls check sql description")
        return _desc, _result

    def insertRow(self, table_name, data):
        """向数据库table_name中插入一行数据data, data必须是字典类型{'xxx': ['xxxx'], 'xxx':['xxxx']}"""
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        self.cur.execute(_sql, tuple(_params))
        self.commit()

    def insertMany(self, table_name, data):
        """向数据库table_name中插入一行数据data, data必须是字典类型{'xxx': ['xx','xxx','xxx','xxx'], 'xxx':['xx','xxx','xxx','xxx']}"""
        """executemany 支持的_params格式， (['xx', 'xxx', 'xxx', 'xxx'],['xx', 'xxx', 'xxx', 'xxx'])"""
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = []
        for i in range(len(data)):
            val = []
            for key in columns:
                val.append(data[key][i])
            _params.append(val)
        self.cur.executemany(_sql, tuple(_params))
        self.commit()

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

    #
    # def rollback(self):
    #     self.conn.rollback()
    #



if __name__ == '__main__':
    mysql = MySQL()
    mysql.selectDb('testdb')
    tbname = 'psmc_lot_tracing_table'
    datas = {'Lot_ID': ['BPH2870A0', 'BPH2870B0'], 'Current_Chip_Name':['AAYRGKS4B-TM01','AAYRGKS4B-TM01']}
    mysql.insertMany(tbname, datas)





