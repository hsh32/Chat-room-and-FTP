import gevent

def foo(a, b):
    print("Running foo...", a, b)
    gevent.sleep(2)


def bar():
    print("Running bar...")
    gevent.sleep(3)
    print("Bar again")


# 封装为协程函数
f = gevent.spawn(foo, 1, "hello")
g = gevent.spawn(bar)
gevent.joinall([f, g])
