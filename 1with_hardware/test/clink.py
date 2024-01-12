'''
    获取单点（区域内）灰度总和
'''

import numpy as np
import cv2 as cv
import tkinter.messagebox as tk


#   鼠标回调函数
def click_circle(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        circle_s, averag_s, circle_m, averag_m, circle_l, averag_l = sum_gray(img_gray, x, y)
        cv.circle(img_gray, center=(x, y), radius=circle_s, color=0, thickness=5)
        cv.circle(img_gray, center=(x, y), radius=circle_m, color=0, thickness=5)
        cv.circle(img_gray, center=(x, y), radius=circle_l, color=0, thickness=5)
        print('============================')
        print('像素坐标：(%s,%s)\r\n'
              '小圆(半径%s)：%.2f\r\n'
              '中圆（半径%s）：%.2f\r\n'
              '大圆（半径%s）：%.2f'
              % (x, y, circle_s, averag_s, circle_m, averag_m, circle_l, averag_l))
        print('============================')
        # print(x,y)
        # print(img_array[y, x])


#   获取范围内灰度值总和
def sum_gray(img, x, y):
    circle_center = (x, y)  # 圆形圆心
    num = 20
    circle_min = 5
    circle_radius = np.zeros(num, dtype=int)
    for i in range(num):
        circle_radius[i] = circle_min + i * 5
    # print(circle_radius)
    # circle_radius_large = 100  # 圆形半径（大）

    gray_number = np.zeros(num, dtype=int)  # 获取灰度像素个数
    gray_sum = np.zeros(num, dtype=int)  # 获取灰度像素数值总和
    gray_averag = np.zeros(num, dtype=int)  # 灰度均值
    x_InitialPoint = x - circle_radius  # 横向初始值
    y_InitialPoint = y - circle_radius  # 纵向初始值
    # 遍历区域内符合要求的像素点
    # for i in range(num):
    #     for j in range(circle_radius[i] * 2 + 1):
    #         for k in range(circle_radius[i] * 2 + 1):
    #             gray_number[i]

    return 1, 1, 1, 1, 1, 1


#   读取图片
img_original = cv.imread('D:\\WorkSpace\\VIDAS\\0pic_datasheet\\V2.4Time2024-01-22\\1.jpeg')
#   输出图像尺寸
print('图片尺寸：（宽 %s，高 %s）\r\n' % (img_original.shape[1], img_original.shape[0]))
#   灰度化
img_gray = cv.cvtColor(img_original, cv.COLOR_RGB2GRAY)

#   获取图像每一点的灰度值
img_array = np.transpose(np.array(img_gray))
#   设置窗口名
cv.namedWindow(winname='drawing', flags=cv.WINDOW_KEEPRATIO)
cv.resizeWindow("drawing", 400, 900) #设置窗口大小
cv.moveWindow("drawing",200,50)
#   设置鼠标回调函数
cv.setMouseCallback('drawing', click_circle)

while True:
    #   显示图片
    cv.imshow('drawing', img_gray)
    # 按 q 键退出
    if cv.waitKey(1) & 0xFF == ord('q'):
        # print(img.shape)
        break
    elif cv.waitKey(1) & 0xFF == ord('w'):
        img_gray = cv.cvtColor(img_original, cv.COLOR_RGB2GRAY)

cv.destroyAllWindows()
