"""
    ftp文件服务器思路分析
    1.技术点分析
        *并发模型 多线程并发模式
        *数据传输

    2.结构设计
        *客户端发起请求,打印请求提示界面
        *文件传输功能封装为类
    3.功能分析
        *网络搭建

        *查看文件库信息
        *下载文件
        *上传文件
        *客户端退出
    4.协议
    L 请求文件列表
    Q 退出
    G 下载
    P 上传
"""

from threading import Thread
from socket import *
import sys
import os
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
FTP = "/home/tarena/month02/concurrent/me/day11/FTP/"  # 文件库路径


# 将客户端请求功能封装为类(指定一个文件夹做文件库)
class FtpServer:
    def __init__(self, connfd, FTP_PATH):
        self.connfd = connfd
        self.path = FTP_PATH

    def do_list(self):
        # 获取文件列表
        files = os.listdir(self.path)
        if not files:
            self.connfd.send("该文件类表为空".encode())
            return
        else:
            self.connfd.send(b"OK")
        fs = ""
        for file in files:
            if file[0] != "." and os.path.isfile(self.path + file):
                fs += file + "\n"
        self.connfd.send(fs.encode())

    def do_get(self, filename):
        try:
            fd = open(self.path + filename, "rb")
        except IOError:
            self.connfd.send("文件不存在".encode())
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b"##")
                break
            self.connfd.send(data)

    def do_put(self, filename):
        if os.path.exists(self.path + filename):
            self.connfd.send("该文件已存在".encode())
            return
        self.connfd.send(b"OK")
        fd = open(self.path + filename, "wb")
        while True:
            data = self.connfd.recv(1024)
            if data == b"##":
                break
            fd.write(data)
        fd.close()


# 客户端请求处理函数
def handle(c):
    cls = c.recv(1024).decode()
    FTP_PATH = FTP + cls + "/"
    ftp = FtpServer(c, FTP_PATH)
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == "Q":
            return
        elif data[0] == "L":
            ftp.do_list()

        elif data[0] == "G":
            filename = data.strip().split(" ")[-1]
            ftp.do_get(filename)

        elif data[0] == "P":
            filename = data.strip().split(" ")[-1]
            ftp.do_put(filename)


# 网络搭建
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("listening on the port 8888")
    while True:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        print("连接中的客户端:", addr)
        # 创建新的进程处理客户端请求

        t = Thread(target=handle, args=(c,))
        t.setDaemon(True)  # 分支线程随主线程退出
        t.start()


if __name__ == "__main__":
    main()
