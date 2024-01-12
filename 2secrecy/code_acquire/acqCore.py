# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
# 主库
# ----------------------------------------------------------------------------#
import sys
from PIL import Image
import os
import datetime
import time
# import frozen as frozen

# ----------------------------------------------------------------------------#
# 设备库
# ----------------------------------------------------------------------------#
import gxipy as gx
import serial
import serial.tools.list_ports


class Acq_Core:

    #   参数
    def __init__(self):
        pass

    #   1 灯源控制器初始化
    def Led_init(self):
        pass

    #   2 摄像头初始化
    def Camera_init(self):
        pass

    #   3 获取缓存图像
    def img_cache(self):
        pass