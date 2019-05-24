"""
    dict
"""
import pymysql
import hashlib
import time


class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 database='dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset

        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    def create_cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    # 处理注册
    def register(self, name, passwd):
        sql = "select * from dict_user where name='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()  # 如果查询到结果
        if r:
            return False

        # 加密处理
        hash = hashlib.md5((name + "!@#$%!^!^)*(_(+").encode())
        hash.update(passwd.encode())

        sql = "insert into dict_user (name,passwd) values (%s,%s)"

        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # 处理登录
    def login(self, name, passwd):
        hash = hashlib.md5((name + "!@#$%!^!^)*(_(+").encode())
        hash.update(passwd.encode())
        sql = "select * from dict_user where name='%s' and passwd='%s'" % (name, hash.hexdigest())

        # 如果查询到结果
        if self.cur.execute(sql):
            return True

    # 插入历史记录
    def insert_history(self, name, word):
        tm = time.ctime()
        sql = "insert into dict_history (name,word,time) values (%s,%s,%s)"
        try:
            self.cur.execute(sql, [name, word, tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 查单词
    def query(self, word):
        sql = "select mean from words where word='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()

        if r:
            return r[0]

    # 查历史
    def history(self, name):
        sql = "select name,word,time from dict_history where name='%s' order by id desc limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()
