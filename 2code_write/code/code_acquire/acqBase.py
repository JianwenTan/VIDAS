# -*- coding: utf-8 -*-
import os


class Acq_Base:

    #   参数
    def __init__(self, path_cache):
        #   图像缓存路径
        self.pathCa = path_cache

    #   1 删除缓存图像
    def clear_cache(self):
        for i in os.listdir(self.pathCa):
            os.remove(self.pathCa + "%s" % i)
        print("缓存图片全部删除")

    #   2 检测缓存图像
    def img_check(self):
        if len(os.listdir(self.pathCa)) == 8:
            print("图片获取完毕")
            return 1
        else:
            return 0
