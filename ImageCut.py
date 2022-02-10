import numpy as np
import time
import cv2
import sys

cap = cv2.VideoCapture(2)
start_time = time.time()

while(True):
    ret, img = cap.read()
    img = cv2.resize(img, (416, 416), interpolation=cv2.INTER_AREA)

    #获取尺寸
    sum_rows = img.shape[0]
    sum_cols = img.shape[1]

    cut_time = time.time()
    send_time = format(cut_time - start_time, '0.4f')
    print(send_time)
    part1 = img[0:sum_rows, 0:sum_cols // 2] #裁图
    part1 = cv2.imencode('.jpg', part1)[1]  #编码
    pic1 = np.array(part1)
    data1 = pic1.tostring()    #格式转换
    print(type(data1))
    dict = {'T':send_time,
            'data':data1}
    new_data = bytes('{}'.format(dict),'utf-8')

    #  接收端反编码
    # str1 = str(new_data, encoding="utf-8")
    # data = eval(str1)   # string转dict类型
    # print(type(data))



    part2 = img[0:sum_rows, sum_cols // 2:sum_cols]
    part2 = cv2.imencode('.jpg', part2)[1]
    pic2 = np.array(part2)
    data2 = pic2.tostring()
    print(sys.getsizeof(data2))



    # final_matrix = np.zeros((sum_rows, sum_cols, 3), np.uint8)
    # final_matrix[0:sum_rows, 0:sum_cols // 2] = part1
    #
    # final_matrix[0:sum_rows, sum_cols // 2:sum_cols] = part2

    cv2.imshow('part1', part1)
    cv2.imshow('part2', part2)
    # cv2.imshow('image', final_matrix)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()