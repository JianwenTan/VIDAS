# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
# 主库
# ----------------------------------------------------------------------------#
import sys

import cv2
from PIL import Image
import os
import datetime
import time
# import frozen as frozen

# ----------------------------------------------------------------------------#
# 设备库
# ----------------------------------------------------------------------------#
# import gxipy as gx
# import serial
# import serial.tools.list_ports


class Image_Acquire:

    # ---------------------------------------------------#
    #   0 参数设置
    # ---------------------------------------------------#
    def __init__(self, path_cache, path_save):
        print("————————————————————————————————————————————————————————————————————")
        print("0    图像获取——开始——初始化参数")
        #   开始时间
        start = time.perf_counter()
        #   图像缓存路径
        self.pathCa = path_cache
        #   图像存储路径
        self.pathSa = path_save
        #   延时
        for _ in range(10000000):
            pass
        #   结束时间
        end = time.perf_counter()
        print("0    图像获取——完成——初始化参数  时间消耗：%.2f s" % (end - start))
        print("————————————————————————————————————————————————————————————————————")

    # ---------------------------------------------------#
    #   7 获取完整图像
    # ---------------------------------------------------#
    def img_acquire(self, name):
        print("————————————————————————————————————————————————————————————————————")
        #   开始时间
        start = time.perf_counter()
        print("1    图像获取——开始——获取图像")
        img = cv2.imread(self.pathCa + "1.jpeg")
        cv2.imwrite(self.pathSa + "%s.jpeg" % name, img)
        #   延时
        for _ in range(400000000):
            pass
        #   结束时间
        end = time.perf_counter()
        print("1    图像获取——完成——获取图像  时间消耗：%.2f s" % (end - start))
        print("————————————————————————————————————————————————————————————————————")
        return 1


if __name__ == '__main__':
    #   参数提供
    path = "./picture/"
    now = datetime.datetime.now()
    time_now = now.strftime("%Y_%m_%d_%H_%M_%S")

    #   初始化
    imgAcq = Image_Acquire(path_cache="./pic_cache/", path_save=path)

    #   程序调用
    imgAcq.img_acquire(name=time_now)
