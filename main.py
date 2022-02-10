#UDP协议测试
#目的：为图传做准备
import sys

import numpy as np
import time
import cv2
import threading
from time import ctime, sleep
import socket

def cutimage(img):
    #获取尺寸
    sum_rows = img.shape[0]
    sum_cols = img.shape[1]

    cut_time = time.time()
    send_time = format(cut_time - start_time, '0.4f')

    part1 = img[0:sum_rows, 0:sum_cols // 2] #裁图
    part1 = cv2.imencode('.jpg', part1)[1]  #编码
    pic1 = np.array(part1)
    data1 = pic1.tostring()    #格式转换

    part2 = img[0:sum_rows, sum_cols // 2:sum_cols]
    part2 = cv2.imencode('.jpg', part2)[1]
    pic2 = np.array(part2)
    data2  = pic2.tostring()

    # 接收端重组图片
    # final_matrix = np.zeros((sum_rows, sum_cols, 3), np.uint8)
    # final_matrix[0:sum_rows, 0:sum_cols // 2] = part1
    #
    # final_matrix[0:sum_rows, sum_cols // 2:sum_cols] = part2

    #cv2.imshow('part1', part1)
    #cv2.imshow('part2', part2)
    # cv2.imshow('image', final_matrix)
    # print(sys.getsizeof(data1))
    return data1, data2

def pipe_1(IP,PORT,data1):
    #length = sys.getsizeof(data)
    #print(str(length) + " Bytes")
    print(IP, PORT)
    socket.sendto(data1, (IP, PORT))
    print("pipe_1 finished " + ctime())
    #sleep(1)

def pipe_2(IP,PORT,data2):
    global list

    socket.sendto(data2, (IP, PORT))
    print("pipe_2 finished " + ctime())
    #sleep(1)

    # ---------------------------------------
    T = time.time()
    data, addr = socket.recvfrom(65500)
    if data:
        Delay = float('%.5f' % ((time.time() - T)/2) )
        list.append(Delay)
        print("dalay_time " + str(np.mean(list)))

def threaded(data1,data2):   #测试完后用类重构
    UDP_IP = "192.168.2.147"

    PORT_1 = 5005
    PORT_2 = 5006

    threads = []
    t1 = threading.Thread(target=pipe_1, args=(UDP_IP, PORT_1,data1))
    threads.append(t1)
    t2 = threading.Thread(target=pipe_2, args=(UDP_IP, PORT_2,data2))
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)         #守护主线程，防止主线程被挂起
        t.start()

    for t in threads:  # 阻塞进程，防止线程被kill
        t.join()

    #print("all over %s" % ctime())


if __name__ == '__main__':
    #全局变量
    list = []
    socket = socket.socket(socket.AF_INET,  # Internet
                           socket.SOCK_DGRAM)  # UDP
    cap = cv2.VideoCapture(2)
    start_time = time.time()
    while (True):
        ret, img = cap.read()
        img = cv2.resize(img, (416, 416), interpolation=cv2.INTER_AREA)
        data1, data2 = cutimage(img)
        threaded(data1, data2)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
