"""
    作业:
    1.编写程序完成效率测试
        使用单线程执行计算密集函数十次,记录时间,执行io密集函数十次记录时间(fun01_c,fun01_i)
            fun01_c执行时间:9.39
            fun01_i执行时间:5.02
        使用10个线程分别执行计算密集函数1次记录时间,执行io密集函数1次记录时间(fun02_c,fun02_i)
            fun02_c执行时间:10.79
            fun02_i执行时间:6.27
        使用10个进程分别执行计算密集函数1次记录时间,执行io密集函数1次记录时间(fun03_c,fun03_i)
            fun03_c执行时间:6.48
            fun03_i执行时间:3.69

        2019.5.13:
        第一次
        fun01_c执行时间:6.39
        fun01_i执行时间:3.03
        fun02_c执行时间:8.73
        fun02_i执行时间:5.14
        fun03_c执行时间:3.43
        fun03_i执行时间:1.5

        第二次
        fun01_c执行时间:6.01
        fun01_i执行时间:3.2
        fun02_c执行时间:8.36
        fun02_i执行时间:5.18
        fun03_c执行时间:3.37
        fun03_i执行时间:1.49

        第三次(终端)
        fun01_c执行时间:5.73
        fun01_i执行时间:3.03
        fun02_c执行时间:8.73
        fun02_i执行时间:5.37
        fun03_c执行时间:3.34
        fun03_i执行时间:1.48


"""
from threading import Thread
from multiprocessing import Process
import time


def time_last(func):
    def wrapper(*args, **kwargs):
        print("%s执行时间:" % func.__name__, end="")
        a = time.time()
        return func(*args, **kwargs), print(round((time.time() - a), 2))

    return wrapper


# 计算密集型函数
def count(x, y):
    c = 0
    while c < 7000000:
        c += 1
        x += 1
        y += 1


def count_10():
    for i in range(10):
        count(1, 1)


# io密集型程序
def io():
    write()
    read()


def io_10():
    for i in range(10):
        io()


def write():
    f = open('.test', 'w')
    for i in range(1500000):
        f.write("hello world\n")
    f.close()


def read():
    f = open('.test')
    f.readlines()
    f.close()


@time_last
def fun01_i():
    t = Thread(target=io_10)
    t.start()
    t.join()


@time_last
def fun01_c():
    t = Thread(target=count_10)
    t.start()
    t.join()


@time_last
def fun02_i():
    jobs = []
    for i in range(10):
        t = Thread(target=io)
        jobs.append(t)
        t.start()
    for i in jobs:
        i.join()


@time_last
def fun02_c():
    jobs = []
    for i in range(10):
        t = Thread(target=count, args=(1, 1))
        jobs.append(t)
        t.start()
    for i in jobs:
        i.join()


@time_last
def fun03_i():
    jobs = []
    for i in range(10):
        p = Process(target=io)
        jobs.append(p)
        p.start()
    for i in jobs:
        i.join()


@time_last
def fun03_c():
    jobs = []
    for i in range(10):
        p = Process(target=count, args=(1, 1))
        jobs.append(p)
        p.start()
    for i in jobs:
        i.join()


def main():
    fun01_c()
    fun01_i()
    fun02_c()
    fun02_i()
    fun03_c()
    fun03_i()


if __name__ == "__main__":
    main()
