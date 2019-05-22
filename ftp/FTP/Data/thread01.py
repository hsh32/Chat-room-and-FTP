"""
    线程示例
"""

import threading
from time import sleep
import os

a = 1


# 线程函数
def music():
    global a
    print("a=", a)
    a = 10000
    for i in range(5):
        sleep(2)

        print(os.getpid(), "表态")


# 创建线程对象
t = threading.Thread(target=music)
t.start()
for i in range(3):
    sleep(3)
    print(os.getpid(), "男孩")
t.join()
print("Main Thread a = ", a)
