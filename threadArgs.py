# coding=utf-8

import threading
from time import ctime, sleep


# 多线程如何返回值
class MyThread1(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread1, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func()

class MyThread2(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread2, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func()


# 多线程
def music():
    while True:
        print("I was listening to music. %s" % ( ctime()))
        #sleep(0.01)


def move():
    while True:
        print("I was at the move! %s" % ( ctime()))
        #sleep(0.01)


threads = []
t1 = MyThread1(music, args=())
threads.append(t1)
t2 = MyThread2(move, args=())
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    print("all over %s" % ctime())