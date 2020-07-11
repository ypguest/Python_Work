# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
设置sql操作相关的类，更新，插入等参数均为dict, 查询参数为list
"""
import MySQLdb as mysql


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
            self.conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
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

    def rollback(self):
        self.conn.rollback()

    def getLastInsertId(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def selectDb(self, db):
        """选择数据库"""
        try:
            self.cur.execute('USE {};'.format(db))
        except:
            raise Exception("db error,please check the sql config.")

    def sqlAll(self, _sql_str, _arg=()):
        try:
            self.cur.execute(_sql_str)
            _result = self.cur.fetchall()
            _desc = self.cur.description
            self.close()
        except:
            raise Exception("fetchRow Error, please check sql description")
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
        _result = list(_result)
        return _desc, _result

    def fetchRow(self, tbname, items='*', condition=()):
        """根据sql语句查询数据库，返回一行结果，并关闭数据库"""
        _items = []
        _arg = []
        _prefix = "SELECT {} FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        if isinstance(condition, tuple):
            _arg = condition
        else:
            _columns = condition.keys()
            for key in condition.keys():
                _items.append("`%s` = %%s" % key)
                _arg.append(condition[key])
            _items = ' and '.join(_items)
        if isinstance(_items, str):
            _sql_str = " WHERE ".join([_prefix, str(_items)])
        else:
            _sql_str = _prefix
        try:
            self.cur.execute(_sql_str, _arg)
            _result = self.cur.fetchone()
            _desc = self.cur.description
            self.close()
            _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
            _result = list(_result)
        except:
            raise Exception("fetchRow Error, please check sql description")
        return _desc, _result

    def fetchAll(self, tbname, items='*', condition=()):
        """根据sql语句查询数据库，返回所有结果，并关闭数据库（表头及数据以list形式返回）"""
        _items = []
        _arg = []
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if items == '*':
            _prefix = "SELECT * FROM `{}`".format(tbname)
        else:
            _prefix = "SELECT {} FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if condition == {} or condition == ():
            _arg = ()
        else:
            _columns = condition.keys()
            for key in condition.keys():
                _items.append("`%s` = %%s" % key)
                _arg.append(condition[key])
            _items = ' and '.join(_items)
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if isinstance(_items, str):
            _sql_str = " WHERE ".join([_prefix, str(_items)])
        else:
            _sql_str = _prefix
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        try:
            self.cur.execute(_sql_str, _arg)
            _result = self.cur.fetchall()
            _desc = self.cur.description           # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
            self.close()
        except:
            raise Exception("fetchRow Error, pls check sql description")
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        _desc = [_desc[i][0] for i in range(len(_desc))]  # 将表头转换为list形式
        _result = [list(i) for i in _result]   # 将数据转换为list形式
        return _desc, _result

    def fetchpage(self, tbname, page=0, size=0, items='*', condition=()):
        """根据sql语句查询数据库，按页返回数据（表头及数据以list形式返回）"""
        _items = []
        _arg = []
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if items == '*':   # 如果选择* 则返回所有 SELECT * FROM tbname
            _prefix = "SELECT * FROM `{}`".format(tbname)
        else:
            _prefix = "SELECT {} FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        # ----生成SELEC Item From tbname WHERE `Item1` = %s AND `Item2` = %s-----------------
        # ----------------------------------------------------------------------------------
        if condition == {} or condition == ():
            _arg = ()
        else:
            _columns = condition.keys()
            for key in condition.keys():
                _items.append("`%s` = %%s" % key)
                _arg.append(condition[key])
            _items = ' and '.join(_items)
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if isinstance(_items, str):
            _sql_str = " WHERE ".join([_prefix, str(_items)])
        else:
            _sql_str = _prefix
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if page != 0 and size != 0:
            _sql_str = _sql_str + ' LIMIT %s,%s' % (size, (page - 1) * size)
        else:
            pass
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        try:
            self.cur.execute(_sql_str, _arg)
            _result = self.cur.fetchall()
            _desc = self.cur.description           # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
            self.close()
        except:
            raise Exception("fetchRow Error, pls check sql description")
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
        _result = [list(i) for i in _result]
        return _desc, _result

    def insertRow(self, tbname, data):
        """向数据库table_name中插入一行数据data, data必须是字典类型{'xxx': ['xxxx'], 'xxx':['xxxx']}"""
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', tbname, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        try:
            self.cur.execute(_sql, tuple(_params))
            self.commit()
        except Exception:
            self.rollback()

    def insertMany(self, tbname, data):
        """向数据库table_name中插入一行数据data, data必须是字典类型{'xxx': ['xx','xxx','xxx','xxx'], 'xxx':['xx','xxx','xxx','xxx']}"""
        """executemany 支持的_params格式， (['xx', 'xxx', 'xxx', 'xxx'],['xx', 'xxx', 'xxx', 'xxx'])"""
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', tbname, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = []
        for i in range(len(data)):
            val = []
            for key in columns:
                val.append(data[key][i])
            _params.append(val)
        try:
            self.cur.executemany(_sql, tuple(_params))
            self.commit()
        except Exception:
            self.rollback()

    def update(self, tbname, data, condition):
        """更新数据库table_name中条件为condition的行，更新的数据为data, data/condtiion均必须是字典类型{'xxx': ['xx','xxx','xxx','xxx'], 'xxx':['xx','xxx','xxx','xxx']}"""
        _data = []
        _condition = []
        _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
        for key in data.keys():
            _data.append("`%s` = '%s'" % (key, data[key]))
        _data = ', '.join(_data)
        for key in condition.keys():
            _condition.append("`%s` = '%s'" % (key, condition[key]))
        _condition = ' and '.join(_condition)
        _sql = " ".join([_prefix, _data, "WHERE", _condition])
        try:
            self.cur.execute(_sql)
            self.commit()
        except Exception:
            self.rollback()

    def delete(self, tbname, condition):
        """删除数据库table_name中条件为condition的行，条件必须是字典类型{'xxx': ['xx','xxx','xxx','xxx'], 'xxx':['xx','xxx','xxx','xxx']}"""
        _condition = []
        _prefix = "".join(['DELETE FROM `', tbname, '` ', 'WHERE'])
        for key in condition.keys():
            _condition.append("`%s` = '%s'" % (key, condition[key]))
        _condition = ' and '.join(_condition)
        _sql = " ".join([_prefix, _condition])
        return self.cur.execute(_sql)


if __name__ == '__main__':
    """用法示例：选取，插入，更新，删除"""
    mysql = MySQL()   # 实例化MySQL, 默认设置为host='localhost', user="root", password="yp*963.", port=3306, charset="utf8")
    mysql.selectDb('configdb')  # 连接数据库

    # """具体操作定义：选取单行或多行"""
    table = 'psmc_product_version'
    item = ['PowerChip_Product_ID']
    mycondition = {'Nick_Name': 'Hanlu'}
    des, mydata = mysql.fetchpage(tbname=table, size=50, page=0, items=item, condition=mycondition)
    mysql.cur.close()

    """具体操作定义：插入单行或多行"""
    # table = 'psmc_lot_tracing_table'
    # data = {'Lot_ID': ['BPH2870A0'], 'Current_Chip_Name': ['AAYRGKS4B-TM01']}
    # mysql.insertRow(table, data)
    # mysql.cur.close()
    # mysql.conn.close()





