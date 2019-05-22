# 功能 : 类似qq群功能
# 【1】 有人进入聊天室需要输入姓名,姓名不能重复
# 【2】 有人进入聊天室时,其他人会收到通知:xxx 进入了聊天室
# 【3】 一个人发消息,其他人会收到:xxx : xxxxxxxxxxx
# 【4】 有人退出聊天室,则其他人也会收到通知:xxx退出了聊天室
# 【5】 扩展功能:服务器可以向所有用户发送公告:管理员消息: xxxxxxxxx

from socket import *
import os
import sys

# 服务器地址
ADDR = ("176.23.6.119", 8888)


def send_msg(s, name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = "quit"
        # 退出聊天室
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出")
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        # 服务端发送EXIT表示让客户端退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode() + "\n发言:", end="")


# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入您的姓名:")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == "__main__":
    main()
