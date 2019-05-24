"""
    gevent 协程演示
    扩展代码
"""
import gevent
from gevent import monkey

monkey.patch_all()

from socket import *


def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b"OK")
    c.close()


s = socket()
s.bind(("0.0.0.0", 8888))
s.listen(5)
print("Listening on the port 8888...")

while True:
    c, addr = s.accept()
    print("Connect from", addr)
    # handle(c) # 循环方案
    gevent.spawn(handle,c) # 协程方案

s.close()
