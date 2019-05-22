from threading import Thread
from time import sleep


def fun():
    sleep(1)
    print("线程属性测试")


t = Thread(target=fun, name="Daemon K")
t.setDaemon(True)

t.start()
# 线程名称
t.setName("Demon K")
print("Thread name:", t.getName())

# 线程生命周期
print("is alive:", t.is_alive())
