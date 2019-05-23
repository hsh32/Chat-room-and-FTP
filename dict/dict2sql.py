import pymysql
import re

fd = open('./dict.txt')
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    database='dict',
    charset='utf8'
)
cur = db.cursor()
sql = 'insert into words (word, mean) values (%s,%s)'

for line in fd:
    tup = re.findall(r'(\S+)\s+(.*)', line)[0]
    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception:
        db.rollback()
fd.close()
cur.close()
db.close()
