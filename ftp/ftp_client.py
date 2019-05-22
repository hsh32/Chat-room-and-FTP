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
"""
from threading import Thread
from socket import *
import sys
import time


# 具体功能
class FtpCLient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')  # 发送请求
        data = self.sockfd.recv(128).decode()  # 等待回复
        if data == "OK":
            data = self.sockfd.recv(4096)
            print(data.decode())

        else:
            print(data)

    def do_get(self, filename):
        self.sockfd.send(('G ' + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            fd = open(filename, "wb")
            while True:
                data = self.sockfd.recv(1024)
                if data == b"##":
                    break
                fd.write(data)
        else:
            print(data)

    def do_put(self, filename):
        try:
            fd = open(filename, "rb")
        except Exception:
            print("文件不存在")
            return
        filename = filename.split("/")[-1]
        self.sockfd.send(("P " + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            fd.close()
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("谢谢使用")


# 发起请求
def request(socket):
    ftp = FtpCLient(socket)
    while True:

        print("输入  :1<Enter>             显示文件")
        print("输入  :2文件名<Enter>       下载文件")
        print("输入  :3文件名<Enter>       上传文件")
        print("输入  :q<Enter>             退出")
        cmd = input("输入命令:")
        if cmd.strip() == "1":
            ftp.do_list()
        elif cmd.strip()[0] == "2":
            filename = cmd.strip().split(" ")[-1]
            ftp.do_get(filename)
        elif cmd.strip()[0] == "3":
            filename = cmd.strip().split(" ")[-1]
            ftp.do_put(filename)
        elif cmd.strip() == "q":
            ftp.do_quit()
        else:
            continue


# 网络连接
def main():
    # 服务器地址:
    ADDR = ("127.0.0.1", 8888)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接服务器失败")
    else:
        print("""
                            
                        FTP系统 版本 1.0
                     维护者 Daemon Kevin 等
                    帮助  可怜的维护者 (ಥ _ ಥ)
        ************************************************
        Data                 File                  Image
        ************************************************
        """)
        cls = input("请输入文件种类:")
        if cls not in ["Data", "File", "Image"]:
            print("Sorry input Error!!!")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)


if __name__ == "__main__":
    main()
