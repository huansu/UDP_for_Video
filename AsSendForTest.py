# 此程序作为前期调试方便写，非本机用，实际NANO使用
import cv2
import socket
import sys
import numpy as np
import time

cap = cv2.VideoCapture(0)

UDP_IP = "192.168.2.147" #接收端IP,接收端保持于此相同IP
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while(True):
    ret, frame = cap.read()
    start = time.time()

    resized = cv2.resize(frame, (416, 416), interpolation=cv2.INTER_AREA)
    pic = cv2.imencode('.jpg', frame)[1]  # 将图片格式转换(编码)成流数据
    pic = np.array(pic)

    data = pic.tostring()    #转为string
    length = sys.getsizeof(data)
    print(str(length) + "Bytes")
    if length > 65536:
        print("超限，请改进压缩办法")
        continue

    else:

        sock.sendto(data, (UDP_IP, UDP_PORT))
        end = time.time()
        FPS = 1/(end - start)
        print(str(int(FPS)) + "FPS")
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()