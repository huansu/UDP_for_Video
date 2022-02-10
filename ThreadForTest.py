#coding=utf-8
# 多线程测试

import threading
from time import ctime, sleep
import socket
import sys

def pipe_1(IP,PORT):
    while True:
        data = b"njnjia"
        #length = sys.getsizeof(data)
        #print(str(length) + " Bytes")
        print(IP, PORT)
        socket.sendto(data, (IP, PORT))
        print("pipe_1 finished " + ctime())
        sleep(1)

def pipe_2(IP,PORT):
    while True:
        data = b"bbbbbb"
        socket.sendto(data, (IP, PORT))
        print("pipe_2 finished " + ctime())
        sleep(1)


if __name__ == '__main__':
    UDP_IP = "192.168.2.147"
    socket = socket.socket(socket.AF_INET,  # Internet
                           socket.SOCK_DGRAM)  # UDP
    PORT_1 = 5005
    PORT_2 = 5006

    threads = []
    t1 = threading.Thread(target=pipe_1, args=(UDP_IP,PORT_1,))
    threads.append(t1)
    t2 = threading.Thread(target=pipe_2, args=(UDP_IP,PORT_2, ))
    threads.append(t2)

    for t in threads:
        #t.setDaemon(True)         #守护主线程，防止主线程被挂起
        t.start()

    for t in threads:          #阻塞进程，防止线程被kill
        t.join()

    print ("all over %s" %ctime())