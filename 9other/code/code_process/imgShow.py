# cython:language_level=3
import numpy as np
import cv2 as cv


class Img_show:

    #   0 参数设置
    def __init__(self):
        pass

    #   1 获取图像，并进行灰度化
    def img_read(self, path_read):
        '''
        参数1 path_read       --图像路径
        返回1 img_original    --原始图像
        '''
        #   读取原始图像，并灰度化
        img_original = cv.cvtColor(cv.imread(path_read), cv.COLOR_RGB2GRAY)
        #   获取图像的宽度和高度
        (w, h) = img_original.shape[:2]
        #   判断图像宽度和高度是否等于5472pix
        if w == 5472 and h ==5472:
            #   获取图像的中心点位
            center = (w // 2, h // 2)
            #   获取图像的旋转矩阵
            M = cv.getRotationMatrix2D(center, -90, 1.0)
            #   旋转图像
            img_original = cv.warpAffine(img_original, M, (w, h))
            #   圈定图像获取区域
            img_original = img_original[0:w, (h - 2300):h]
        else:
            pass

        return img_original

    #   2 图像二值化
    def img_dst(self, img, dat_num):
        '''
        参数1 img         --原始图像
        参数2 dat_num     --二值化阈值
        返回1 img_thres   --二值化图像
        '''
        #   二值化图像
        ret, img_thres = cv.threshold(img, dat_num, 255, cv.THRESH_BINARY)

        return img_thres

    #   3 图像腐蚀
    def img_erosion(self, img, num_erosion):
        '''
        参数1 img             --图像
        参数2 num_erosion     --腐蚀核（3,7,9,11）
        返回1 img_erosion     --腐蚀后图像
        '''
        #   设置图像腐蚀核系数
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_erosion, num_erosion))
        #   图像腐蚀
        img_erosion = cv.erode(img, kernel)

        return img_erosion

    #   4 图像膨胀
    def img_dilation(self, img, num_dilation):
        '''
        参数1 img             --图像
        参数2 num_erosion     --膨胀核（3,7,9,11）
        返回1 img_erosion     --膨胀后图像
        '''
        #   设置图像膨胀核系数
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_dilation, num_dilation))
        #   图像膨胀
        img_dilation = cv.dilate(img, kernel)

        return img_dilation
