"""
    dict 服务端部分
    处理请求逻辑
"""

from multiprocessing import Process
from socket import *
import signal
import sys
from operation_db import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)

def do_register(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b"FAIL")

def do_login(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b"FAIL")

def do_request(c, db):
    db.create_cursor() # 生成游标 db.cur
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if data[0] == 'R':
            do_register(c,db,data)
        if data[0] == 'L':
            do_login(c,db,data)



def main():
    # 创建数据库连接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port 8000")
    while True:
        try:
            c, addr = s.accept()
            print("Connect from:", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
