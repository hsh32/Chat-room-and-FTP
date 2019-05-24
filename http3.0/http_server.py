"""
    http server 3.0
    技术点:
        1.使用tcp通信
        2.select io多路复用

    结构:
        1.采用类封装

    类的接口设计:
        1.在用户使用角度进行工作流程设计
        2.尽可能提供全面的功能,能为用户决定的在类中实现
        3.不能替用户决定的变量可以通过实例化对象传入类中
        4.不能替用户决定的复杂功能,可以通过重写让用户自己决定
"""

from socket import *
from select import select


# 封装功能
class HTTPServer:
    def __init__(self, server_address, static_dir):
        self.server_address = server_address
        self.static_dir = static_dir
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.sockfd.bind(self.server_address)
        self.ip = self.server_address[0]
        self.port = self.server_address[1]

    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    print("Connect from", addr)
                    self.rlist.append(c)
                else:
                    # 处理浏览器请求
                    self.handle(r)

    def handle(self, connfd):
        # 接收http请求;
        request = connfd.recv(4096)
        # print(request.decode())
        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return
        # 请求解析
        request_line = request.splitlines()[0]
        info = request_line.decode().split(" ")[1]
        print(connfd.getpeername(), ":", info)

        # info 分为访问网页和其他
        if info == "/" or info[-5:] == ".html":
            self.get_html(connfd, info)
        else:
            self.get_data(connfd, info)

        self.rlist.remove(connfd)
        connfd.close()

    # 处理网页
    def get_html(self, connfd, info):
        if info == "/":
            filename = self.static_dir + "/index.html"
        else:
            filename = self.static_dir + info
        try:
            fd = open(filename)
        except Exception:
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "\r\n"
            responseBody = "<h1>Sorry,Not Found the page</h1>"
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "\r\n"
            responseBody = fd.read()

        finally:
            response = responseHeaders + responseBody
            connfd.send(response.encode())

    def get_data(self, connfd, info):
        filename = self.static_dir + info
        try:
            fd = open(filename,'rb')
        except Exception:
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "\r\n"
            responseBody = "<h1>Sorry,Not Found the page</h1>"
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "\r\n"
            responseBody = fd.read().decode()
        finally:
            response = responseHeaders + responseBody
            connfd.send(response.encode())


if __name__ == "__main__":
    # 用户自己决定: 地址,内容
    server_addr = ("0.0.0.0", 8000)  # 服务器地址
    static_dir = "./static"  # 网页存放位置

    httpd = HTTPServer(server_addr, static_dir)  # 生成实例对象
    httpd.serve_forever()
