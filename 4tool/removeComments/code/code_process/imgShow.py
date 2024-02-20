import numpy as np
import cv2 as cv


class Img_show:

    def __init__(self):
        pass

    def img_read(self, path_read):
        
        img_original = cv.cvtColor(cv.imread(path_read), cv.COLOR_RGB2GRAY)
        (w, h) = img_original.shape[:2]
        if w == 5472 and h ==5472:
            center = (w // 2, h // 2)
            M = cv.getRotationMatrix2D(center, -90, 1.0)
            img_original = cv.warpAffine(img_original, M, (w, h))
            img_original = img_original[0:w, (h - 2300):h]
        else:
            pass

        return img_original

    def img_dst(self, img, dat_num):
        
        ret, img_thres = cv.threshold(img, dat_num, 255, cv.THRESH_BINARY)

        return img_thres

    def img_erosion(self, img, num_erosion):
        
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_erosion, num_erosion))
        img_erosion = cv.erode(img, kernel)

        return img_erosion

    def img_dilation(self, img, num_dilation):
        
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_dilation, num_dilation))
        img_dilation = cv.dilate(img, kernel)

        return img_dilation
