# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
设置所有sql操作相关的类，更新，插入等参数均为dict, 查询参数为list
"""
import pandas as pd
import MySQLdb as mysql
import sqlite3


class MySQL(object):

    # server
    def __init__(self, host='172.21.21.8', user="root", password="uniic2020", port=3306, charset="utf8"):

    # local
    # def __init__(self, host='localhost', user="root", password="yp*963.", port=3306, charset="utf8"):

        """实例化后自动连接至数据库"""
        # ==== 初始化参数 ====
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset

        self.confgdb = 'configdb'
        self.loaderdb = 'loader'
        self.testdb = 'testdb'

        self.testdb_config = {'user': self.user, 'password': self.password, 'host': self.host, 'database': self.testdb, 'charset': self.charset}

        self.loaderengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, self.loaderdb, self.charset)
        self.testdbengine = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset={}'.format(self.user, self.password, self.host, self.port, self.testdb, self.charset)

    # ==== 连接mysql ====
        try:
            self.conn = mysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)
        self.conn.autocommit(False)  # 设置取消自动提交事务

    def selectDb(self, database='testdb'):
        """选择数据库"""
        try:
            self.cur.execute('USE {};'.format(database))
        except Exception as e:
            print(e)

    def sqlAll(self, _sql_str, _arg=()):
        """查询数据库，并获取所有查询到的表头和结果"""
        try:
            self.cur.execute(_sql_str)
            _result = self.cur.fetchall()
            _desc = self.cur.description
        except Exception as e:
            print(e)
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
            _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
            _result = list(_result)
        except Exception as e:
            print(e)
        return _desc, _result

    def fetchAll(self, tbname, items='*', condition=()):
        """根据sql语句查询数据库，返回所有结果，并关闭数据库（表头及数据以list形式返回）"""
        _anditems = []
        _oritems = []
        _arg = []
        # ======================== 处理SQL语句SELECT XX FROM XX =============================
        if items == '*':
            _prefix = "SELECT * FROM `{}`".format(tbname)
        else:
            _prefix = "SELECT {} FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        # ------------------------处理WHERE后续的部分--------------------------------------------
        # ----------------------------------------------------------------------------------
        if condition == {} or condition == ():  # 如果输入的是空字典，或空的元素
            _arg = ()
        else:
            _columns = condition.keys()  # WHERE 条件的名字['Current_Chip_Name', 'MLot_ID'...]

            for key in condition.keys():  # 遍历WHERE条件, 目前只有'Current_Chip_Name'
                _items = []
                for i in range(len(condition[key])):  # 目前'Current_Chip_Name' 有两个元素
                    _items.append("`%s` = %%s" % key)  # 生成list['`Current_Chip_Name` = %s', '`Current_Chip_Name` = %s']
                    _arg.append(condition[key][i])  # 生成list['AAYRGKS3B-0K01', 'AAYRGKS3B-0L01']
                _oritems.append(' OR '.join(_items))
            _anditems = '(' + ') AND ('.join(_oritems) + ')'
        # ======================= 用WHERE将前后部分连接 ===================================
        if isinstance(_anditems, str):
            _sql_str = " WHERE ".join([_prefix, str(_anditems)])
        else:
            _sql_str = _prefix
        # =================================================================================
        try:
            self.cur.execute(_sql_str, _arg)
            _result = self.cur.fetchall()
            _desc = self.cur.description  # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
        except Exception as e:
            raise print(e)
        # =================================================================================

        _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
        _result = [list(i) for i in _result]
        return _desc, _result

    def dataCount(self, tbname, items='*', condition=()):
        """根据sql语句查询数据库，返回所有结果，并关闭数据库（表头及数据以list形式返回）"""
        _anditems = []
        _oritems = []
        _arg = []
        # ------------------------处理SQL语句SELECT XX FROM XX-------------------------------
        # ----------------------------------------------------------------------------------
        if items == '*':
            _prefix = "SELECT count(*) FROM `{}`".format(tbname)
        else:
            _prefix = "SELECT count({}) FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        # ------------------------处理WHERE后续的部分--------------------------------------------
        # ----------------------------------------------------------------------------------
        if condition == {} or condition == ():  # 如果输入的是空字典，或空的元素
            _arg = ()
        else:
            _columns = condition.keys()  # WHERE 条件的名字['Current_Chip_Name', 'MLot_ID'...]
            for key in condition.keys():  # 遍历WHERE条件, 目前只有'Current_Chip_Name'
                _items = []
                for i in range(len(condition[key])):  # 目前'Current_Chip_Name' 有两个元素
                    _items.append("`%s` = %%s" % key)  # 生成list['`Current_Chip_Name` = %s', '`Current_Chip_Name` = %s']
                    _arg.append(condition[key][i])  # 生成list['AAYRGKS3B-0K01', 'AAYRGKS3B-0L01']
                _oritems.append(' OR '.join(_items))
            _anditems = '(' + ') AND ('.join(_oritems) + ')'

        # -------------------------用WHERE将前后部分连接--------------------------------------
        # ----------------------------------------------------------------------------------
        if isinstance(_anditems, str):
            _sql_str = " WHERE ".join([_prefix, str(_anditems)])
        else:
            _sql_str = _prefix
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        try:
            self.cur.execute(_sql_str, _arg)
            _count = self.cur.fetchall()
        except Exception as e:
            raise print(e)
        return int(_count[0][0])

    def fetchpage(self, tbname, page=0, size=0, items='*', condition=()):
        """根据sql语句查询数据库，按页返回数据（表头及数据以list形式返回）, 同时去除Qty = 0"""
        _anditems = []
        _oritems = []
        _arg = []
        # ------------------------处理SQL语句SELECT XX FROM XX-------------------------------
        # ----------------------------------------------------------------------------------
        if items == '*':
            _prefix = "SELECT * FROM `{}`".format(tbname)
        else:
            _prefix = "SELECT {} FROM `{}`".format(", ".join("".join(['`', _, '`']) for _ in items), tbname)
        # ------------------------处理WHERE后续的部分--------------------------------------------
        # ----------------------------------------------------------------------------------
        if condition == {} or condition == ():  # 如果输入的是空字典，或空的元素
            _arg = ()
        else:
            _columns = condition.keys()  # WHERE 条件的名字['Current_Chip_Name', 'MLot_ID'...]
            for key in condition.keys():  # 遍历WHERE条件, 目前只有'Current_Chip_Name'
                _items = []
                for i in range(len(condition[key])):  # 目前'Current_Chip_Name' 有两个元素
                    _items.append("`%s` = %%s" % key)  # 生成list['`Current_Chip_Name` = %s', '`Current_Chip_Name` = %s']
                    _arg.append(condition[key][i])  # 生成list['AAYRGKS3B-0K01', 'AAYRGKS3B-0L01']
                _oritems.append(' OR '.join(_items))
            _anditems = '(' + ') AND ('.join(_oritems) + ')'
        # -------------------------用WHERE将前后部分连接--------------------------------------
        # ----------------------------------------------------------------------------------
        if isinstance(_anditems, str):
            _sql_str = " WHERE ".join([_prefix, str(_anditems)]) + "and Qty != 0 ORDER BY `Current_Time` DESC"
        else:
            _sql_str = _prefix + 'ORDER BY `Current_Time` DESC'
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        if page != 0 and size != 0:
            _sql_str = _sql_str + ' LIMIT %s,%s' % ((page - 1) * size, page * size)
        else:
            pass
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        try:
            self.cur.execute(_sql_str, _arg)
            _result = self.cur.fetchall()
            _desc = self.cur.description  # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
        except Exception as e:
            raise print(e)
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


class MySQLite(object):

    def __init__(self):
        # ==== 连接SQlite3 ====
        file_path = r'./db/database.db'  # 当前Sqlite路径
        try:
            self.conn = sqlite3.connect(file_path)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def update_df(self, data):
        """将df写入数据库"""
        pd.io.sql.to_sql(data, "tempdb", con=self.conn, if_exists='replace')
        self.conn.close()

    def fetchAll(self, tabinfor):
        """将数据库中的数据全部返回"""
        _sql = 'SELECT * FROM {}' .format(tabinfor)
        try:
            self.cur.execute(_sql)
            _result = self.cur.fetchall()
            _desc = self.cur.description  # description包含name, type_code, display_size, internal_size, precision, scale, null_ok
        except Exception as e:
            raise print(e)
        # ==== 将获取到的数据转化成为列表 ====
        _desc = [_desc[i][0] for i in range(len(_desc))]  # 获取表头
        _result = [list(i) for i in _result]
        return _desc, _result


if __name__ == '__main__':

    """用法示例：选取，插入，更新，删除
    mysql = MySQL()  # 实例化MySQL
    mysql.selectDb('testdb')  # 连接数据库
    
    # ==== 具体操作定义：选取单行或多行 ====
    table = 'psmc_lot_tracing_table'
    item = ['Current_Chip_Name']
    mycondition = {'Current_Chip_Name': ['AAYRGKS2B-TD01', 'AAYRGKS3B-TH01', 'AAYRGKS3B-TL01'], 'Mlot_ID': ['BKL352', 'BKL351']}
    count = mysql.dataCount(tbname=table, items=item, condition=mycondition)
    mysql.cur.close()

    # ==== 具体操作定义：插入单行或多行 ====
    table = 'psmc_lot_tracing_table'
    data = {'Lot_ID': ['BPH2870A0'], 'Current_Chip_Name': ['AAYRGKS4B-TM01']}
    mysql.insertRow(table, data)
    mysql.cur.close()
    mysql.conn.close()
    """
