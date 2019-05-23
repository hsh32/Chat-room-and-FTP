"""
    dict 客户端
    发起请求,展示结果
"""

from socket import *
from getpass import getpass

ADDR = ('127.0.0.1', 8000)
# 所有函数都用s
s = socket()
s.connect(ADDR)

# 二级界面
def login(name):
    while True:
        print("""
        ===============Query============
        1.查单词      2.历史记录     3.注销
        ================================
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            pass
        elif cmd == "2":
            pass
        elif cmd == "3":
            return
        else:
            print("请输入正确的命令!")


# 注册
def do_register():
    while True:
        name = input("User:")
        passwd = getpass()
        passwd1 = getpass("Again:")

        if (" " in name) or (" " in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")

        msg = "R %s %s" % (name, passwd)
        # 发送请求
        s.send(msg.encode())
        # 接收反馈
        data = s.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return

# 登录
def do_login():
    name = input("User:")
    passwd = getpass()
    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())
    #等待反馈
    data = s.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")



# 创建网络连接
def main():
    while True:
        print("""
        =============Welcome============
        1.注册        2.登录        3.退出
        ================================
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            return
        else:
            print("请输入正确的命令!")


if __name__ == '__main__':
    main()
