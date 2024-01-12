import math
import operator
import time

import numpy
import numpy as np
import cv2 as cv
import os
from PIL import Image
import datetime

#   定位点圈定区域，可修改，可删除
roi_position = [
    [0, 300], [0, 2500]  # [startY, endY] [StartX, endX]
]


class Image_Processing:

    #   0 参数设置
    def __init__(self, roi_position):
        #   定位点圈定区域，可修改
        roi_pos = [
            [0, 250], [0, 2500]  # [startY, endY] [StartX, endX]
        ]
        #   定位点的兴趣区间
        self.__roiPos = roi_pos
        #   定义灰度阈值
        self.gray_value = 0
        #   ROI下移数值
        self.gray_down = 0
        #   图片旋转角度
        self.dip_angle = 0
        #   环境灰度值
        self.gray_round = 0

    #   1.1 图像旋转
    def __rotate_img(self, img, angle):
        h, w = img.shape[:2]
        rotate_center = (w / 2, h / 2)
        #   获取旋转矩阵
        #   参数1为旋转中心点；
        #   参数2为旋转角度，正值-逆时针旋转；负值-顺时针旋转；
        #   参数3为各向同性的比例因子，1.0原图，2.0变成原来的2倍，0.5变成原来的0.5倍
        M = cv.getRotationMatrix2D(rotate_center, angle, 1.0)
        #   计算图像新边界
        new_w = int(h * np.abs(M[0, 1]) + w * np.abs(M[0, 0]))
        new_h = int(h * np.abs(M[0, 0]) + w * np.abs(M[0, 1]))
        #   调整旋转矩阵以考虑平移
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2

        rotated_img = cv.warpAffine(img, M, (new_w, new_h))
        return rotated_img

    #   1.2 获取范围内灰度值总和
    def __sum_gray(self, img, x, y, radius):
        '''
                img     --图像转化为灰度数值
                x       --横轴坐标
                y       --纵轴坐标
                radius  --圈定区域半径
                return  --圈定区域灰度均值
                '''
        gray_number = 0  # 获取灰度像素个数
        gray_sum = 0  # 获取灰度像素数值总和
        x_InitialPoint = x - radius  # 横向初始值
        y_InitialPoint = y - radius  # 纵向初始值
        #   查看圈定灰度区域是否超过阈值
        if (x + radius) >= img.shape[0] or (y + radius) >= img.shape[1]:
            return 0
        else:
            # 遍历区域内符合要求的像素点
            for i in range(radius * 2 + 1):
                for j in range(radius * 2 + 1):
                    gray_number += 1
                    gray_sum += img[x_InitialPoint + i, y_InitialPoint + j]
        return gray_sum  # 灰度值总和

    #   1.3 获取范围内灰度值总和的均值
    def __sum_gray_ave(self, img, x, y, radius):
        '''
                img     --图像转化为灰度数值
                x       --横轴坐标
                y       --纵轴坐标
                radius  --圈定区域半径
                return  --圈定区域灰度均值
                '''
        gray_number = 0  # 获取灰度像素个数
        gray_sum = 0  # 获取灰度像素数值总和
        gray_ave = 0
        x_InitialPoint = x - radius  # 横向初始值
        y_InitialPoint = y - radius  # 纵向初始值
        #   查看圈定灰度区域是否超过阈值
        if (x + radius) >= img.shape[0] or (y + radius) >= img.shape[1]:
            return 0
        else:
            # 遍历区域内符合要求的像素点
            for i in range(radius * 2 + 1):
                for j in range(radius * 2 + 1):
                    gray_number += 1
                    gray_sum += img[x_InitialPoint + i, y_InitialPoint + j]
        gray_ave = int(gray_sum / gray_number * 100) / 100
        return gray_ave  # 灰度值总和

    #   1.4 删除缓存图片
    def __clear_cache(self, path):
        os.remove(path)

    #   1.5 获取环境灰度值
    def __gray_round(self, img):
        gray_number = 0  # 获取灰度像素个数
        gray_sum = 0  # 获取灰度像素数值总和
        gray_ave = 0  # 灰度像素均值
        x_InitialPoint = 800  # 横向初始值
        x_length = 600  # 横向长度
        y_InitialPoint = 300  # 纵向初始值
        y_length = 100  # 纵向长度
        #   图像转换为灰度值数组
        img_array = np.transpose(np.array(img))
        #   总和区域内的灰度值
        for i in range(x_length):
            for j in range(y_length):
                gray_number += 2
                gray_sum += img_array[x_InitialPoint + i, y_InitialPoint + j]
                gray_sum += img_array[x_InitialPoint + i, y_InitialPoint + 4700 + j]
        #   计算区域内灰度值均值
        gray_ave = gray_sum / gray_number
        self.gray_round = int(gray_ave * 100) / 100
        num = int(gray_ave / 10) * 10 + 100

        return num

    #   1.6 输出试剂点X轴坐标
    def __point_X(self, min, mid, max):
        point = [0] * 5
        point[0] = min
        point[1] = min + (mid - min) / 2
        point[2] = mid
        point[3] = max - (max - mid) / 2
        point[4] = max
        return point

    #   1.7 改变图像尺寸
    def img_resize(self, img_path, img_name):
        img = Image.open("%s" % img_path)
        #   获取图像尺寸
        width, height = img.size
        #   创建画布
        background = Image.new('L', (height, height))
        #   设定位置
        length = int((height - width) / 2)
        #   放置图像
        background.paste(img, (length, 1))
        #   缩小图像
        background = background.resize((350, 350))
        #   保存图像
        background.save("%s" % img_name)
        return 0

    #   1.8 获取二维矩阵中最小值
    def find_min_value(self, arr):
        #   删除矩阵第一行数据
        arr = np.delete(arr, 0, axis=0)
        min_value = arr[0][0]
        for row in arr:
            for num in row:
                if num < min_value:
                    min_value = num
        print("背景值-扣除：", int(min_value))
        return min_value

    #   1.9 过敏原性质判定
    def nature_positive_negative(self, g_arr, n_arr, comb):
        #   删除矩阵第一行数据
        # g_arr = np.delete(g_arr, 0, axis=0)
        for i in range(9):
            for j in range(5):
                if i > 0 or j == 2:
                    if g_arr[i][j] < 60000:
                        n_arr[i][j] = "阴性"
                    elif g_arr[i][j] < 660000:
                        n_arr[i][j] = "弱阳性"
                    elif g_arr[i][j] < 1100000:
                        n_arr[i][j] = "中阳性"
                    elif g_arr[i][j] > 1100000:
                        n_arr[i][j] = "强阳性"
                    else:
                        n_arr[i][j] = "error"
        return n_arr

    #   2.1 获取图像，并进行灰度化
    def img_read(self, path_read):
        '''
                input:  图像路径
                ouput:  原始图像
                '''
        #   读取原始图像，并灰度化
        img_original = cv.cvtColor(cv.imread(path_read), cv.COLOR_RGB2GRAY)
        #   顺时针旋转90度
        (w, h) = img_original.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, -90, 1.0)
        img_original = cv.warpAffine(img_original, M, (w, h))
        #   圈定图像获取区域
        img_original = img_original[0:w, (h - 2300):h]

        return img_original

    #   2.2 图像二值化
    def img_dst(self, img, dat_num):
        '''
                input：  原始图像，二值化阈值
                output： 二值化图像
                '''
        #   二值化图像
        ret, img_thres = cv.threshold(img, dat_num, 255, cv.THRESH_BINARY)

        return img_thres

    #   2.3 图像腐蚀
    def img_erosion(self, img, num_erosion):
        '''
        input：  图像，腐蚀核（3,7,9,11）
        output： 腐蚀后图像
        '''
        #   图像腐蚀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_erosion, num_erosion))
        img_erosion = cv.erode(img, kernel)

        return img_erosion

    #   2.4 图像膨胀
    def img_dilation(self, img, num_dilation):
        '''
        input：  图像，膨胀核（3,7,9,11）
        output： 膨胀后图像
        '''
        #   图像腐蚀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_dilation, num_dilation))
        img_dilation = cv.erode(img, kernel)

        return img_dilation

    #   3.1 初次获取定位点
    def img_location_first(self, img_gray, img_dst, num, flag):
        # 参数设置
        num_down = 0
        len_down = 50  # 单次下移量
        circle_x = []
        circle_y = []
        circle_r = []
        for i in range(num):
            num_down = len_down * i  # 总下移量
            #   获取ROI感兴趣区间
            img_ROI = img_dst[(self.__roiPos[0][0] + num_down):(self.__roiPos[0][1] + num_down),
                      self.__roiPos[1][0]:self.__roiPos[1][1]]

            # starttime = datetime.datetime.now()
            circle = cv.HoughCircles(img_ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
            # endtime = datetime.datetime.now()
            # time_use = (endtime - starttime).seconds * 1000 + (endtime - starttime).microseconds / 1000
            # print('funtion time use:%dms' % (time_use))
            # if time_use >= 100:
            #     break

            #   当前ROI未找到定位点
            if circle is None:
                continue
            elif circle.shape[1] < 3:
                continue
            #   当前ROI找到全部定位点
            elif circle.shape[1] >= 3:
                #   定位点坐标+ROI定位区间
                for i in range(circle.shape[1]):
                    circle[0][i][0] = circle[0][i][0] + self.__roiPos[1][0]
                    circle[0][i][1] = circle[0][i][1] + self.__roiPos[0][0] + num_down
                #   定位点坐标划分为x，y
                for j in circle[0, :]:
                    circle_x.append(j[0])
                    circle_y.append(j[1])
                    circle_r.append(j[2])

                #   退出标志为0
                exit_flag = 0

                #  标志1：检测定位点Y轴，像素误差大于200
                circle_y_sort = sorted(circle_y, key=float)
                diff_x1 = np.diff(circle_y_sort)
                for i in range(len(diff_x1)):
                    if diff_x1[i] > 200:
                        exit_flag += 1
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：", exit_flag)
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                #   标志2：检测定位点X轴，像素误差小于630
                circle_x_sort = sorted(circle_x, key=float)
                diff_x2 = np.diff(circle_x_sort)
                for i in range(len(diff_x2)):
                    if diff_x2[i] < 630:
                        exit_flag += 2
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：", exit_flag)
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                #   标志3：检测定位点的灰度值均值，灰度均值误差大于20
                if circle.shape[1] == 3:
                    gray_posi = np.zeros(1 * 3)
                    img_array = np.transpose(np.array(img_gray))
                    for j in range(3):
                        gray_posi[j] = self.__sum_gray_ave(img_array, int(circle_x[j]), int(circle_y[j]),
                                                           int(circle_r[j]))
                    min_index, min_number = min(enumerate(gray_posi), key=operator.itemgetter(1))
                    max_index, max_number = max(enumerate(gray_posi), key=operator.itemgetter(1))
                    if (max_number - min_number) >= 20:
                        exit_flag += 4
                else:
                    gray_posi = np.zeros(1 * circle.shape[1])
                    exit_flag += 4

                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：", exit_flag)
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue
                else:
                    self.gray_down = num_down
                    print("---------------------")
                    print("* 初次获取定位点")
                    print("区间下移量：", num_down)
                    print("定位点X轴坐标：", circle_x)
                    print("定位点X轴差值：", diff_x2)
                    print("定位点Y轴坐标：", circle_y)
                    print("定位点直径：", circle_r)
                    print("定位点灰度值：", gray_posi)
                    if flag == 1:
                        # 圈定ROI区域
                        cv.rectangle(img_gray, pt1=(self.__roiPos[1][0], self.__roiPos[0][0] + num_down),
                                     pt2=(self.__roiPos[1][1], self.__roiPos[0][1] + num_down), color=(0, 0, 0),
                                     thickness=20)
                        for j in circle[0, :]:
                            cv.circle(img_gray, (int(j[0]), int(j[1])), int(j[2]), (0, 0, 0), 10)
                    return 1, img_gray, circle, circle_x, circle_y
        # 未找到定位点
        return 0, img_gray, 0, 0, 0

    #   3.2 矫正图像角度
    def img_correct_first(self, img_gray, img_dst, circle_x, circle_y):
        min_index, min_number = min(enumerate(circle_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(circle_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i

        #   计算直线上的垂足点与中间点的角度，然后根据角度旋转图像
        angle = math.atan2(circle_y[max_index] - circle_y[min_index], circle_x[max_index] - circle_x[min_index])
        angle = angle * 180 / math.pi
        self.dip_angle = angle
        print("---------------------")
        print("定位点倾斜角度：", angle)
        #   旋转图像
        img_rota = self.__rotate_img(img_gray, angle)
        img_rota_dst = self.__rotate_img(img_dst, angle)

        return img_rota, img_rota_dst, middle_index

    #   3.3 验证定位点
    def img_correct_second(self, img_gray, img_dst, circle_x, circle_y, flag):
        cir_x = []
        cir_out_x = []
        cir_y = []
        cir_out_y = []
        cir_r = []
        exit_flag = 0
        dis_error = 0
        point_x = [0] * 5
        point_y = [450, 750, 1100, 1430, 1770, 2100, 2450, 2780]
        #   图像矫正后，获取Y轴参考点
        y_arve = int(sum(circle_y) / 3) - 100
        print("---------------------")
        print("参考点Y轴：", y_arve)
        #   获取参考点区间范围
        ROI = img_dst[(y_arve):(y_arve + 200), 0:2500]
        #   获取区间范围的定位点
        circle = cv.HoughCircles(ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50, maxRadius=150)
        #   检测失败，直接返回
        if (circle is None) or (circle.shape[1] < 3):
            min_in, min_num = min(enumerate(circle_x), key=operator.itemgetter(1))
            max_in, max_num = max(enumerate(circle_x), key=operator.itemgetter(1))
            middle_index = None
            for i in range(3):
                if i == min_in or i == max_in:
                    continue
                else:
                    middle_index = i
            #   输出X轴坐标
            point_x = self.__point_X(min_num, circle_x[middle_index], max_num)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            for i in range(8):
                point_y[i] = int(y_arve + point_y[i])
            return point_x, point_y, dis_error, circle_x, circle_y
        #   整理定位点的数据
        for i in circle[0, :]:
            cir_x.append(i[0])
            cir_y.append(i[1] + y_arve)
            cir_r.append(i[2])
        print("矫正后定位点X轴坐标：", cir_x)
        print("矫正后定位点Y轴坐标：", cir_y)
        print("矫正后定位点直径：", cir_r)
        #   定位点灰度均值
        gray_posi = [0] * 3
        img_array = np.transpose(np.array(img_gray))
        for j in range(3):
            gray_posi[j] = self.__sum_gray_ave(img_array, int(cir_x[j]), int(cir_y[j]), int(cir_r[j]))
        gray_ave = int((sum(gray_posi) / 3) * 100) / 100 - 20
        print("定位点灰度均值判读阈值：", gray_ave)

        #   画图
        if flag == 1:
            for j in circle[0, :]:
                cv.circle(img_gray, (int(j[0]), int(j[1] + y_arve)), int(j[2]), (0, 0, 0), 10)
            cv.rectangle(img_gray, pt1=(0, (y_arve)), pt2=(2500, (y_arve + 200)), color=(0, 0, 0), thickness=20)

        #   X轴定位点
        min_index, min_number = min(enumerate(cir_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(cir_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i
        cir_out_x = [cir_x[min_index], cir_x[middle_index], cir_x[max_index]]
        cir_out_y = [cir_y[min_index], cir_y[middle_index], cir_y[max_index]]
        #   底部试剂点位置
        y_down = 2900
        #   底部左边试剂点位置
        ROI_Min = img_dst[(y_arve + y_down - 170):(y_arve + y_down + 170), int(min_number - 150):int(min_number + 150)]
        circle_min = cv.HoughCircles(ROI_Min, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
        #   底部右边试剂点位置
        ROI_Max = img_dst[(y_arve + y_down - 170):(y_arve + y_down + 170), int(max_number - 150):int(max_number + 150)]
        circle_max = cv.HoughCircles(ROI_Max, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
        print("---------------------")
        print("* 判断底部定位点情况")
        #   底部定位点均不存在
        if circle_min is None and circle_max is None:
            print("底部全部定位点不存在")
            exit_flag = 3
        #   左侧定位点不存在
        elif circle_min is None:
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            max_gray_aver = self.__sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
            print("右侧定位点的灰度均值：", max_gray_aver)
            print("底部定位点右边点坐标：" + "(%d" % x_max + ",%d)" % y_max)
            if max_gray_aver <= gray_ave:
                exit_flag = 3
            else:
                exit_flag = 2
        #   右侧定位点不存在
        elif circle_max is None:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            min_gray_aver = self.__sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
            print("左侧定位点的灰度均值：", min_gray_aver)
            print("底部定位点左边点坐标：" + "(%d" % x_min + ",%d)" % y_min)
            if min_gray_aver <= gray_ave:
                exit_flag = 3
            else:
                exit_flag = 1
        #   底部定位点均存在
        else:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            min_gray_aver = self.__sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
            max_gray_aver = self.__sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
            print("左侧定位点的灰度均值：", min_gray_aver)
            print("右侧定位点的灰度均值：", max_gray_aver)
            print("底部定位点左边点坐标：" + "(%d" % x_min + ",%d)" % y_min)
            print("底部定位点右边点坐标：" + "(%d" % x_max + ",%d)" % y_max)
            if min_gray_aver <= gray_ave:
                exit_flag += 2
            if max_gray_aver <= gray_ave:
                exit_flag += 1

        print("---------------------")
        print("* 输出底部存在的定位点")
        #   底部定位点均存在
        if exit_flag == 0:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            #   画出位置，可注释
            cv.circle(img_gray, (int(x_min), int(y_min)), int(circle_min[0, :][0][2]), (0, 0, 0), 10)
            cv.circle(img_gray, (int(x_max), int(y_max)), int(circle_max[0, :][0][2]), (0, 0, 0), 10)
            # 试剂点X轴方向误差
            dis_error = ((x_min - min_number) + (x_max - max_number)) / 2
            print("试剂点X轴坐标误差值：", dis_error)
            #   输出X轴坐标
            point_x = self.__point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            y_arve_new = sum(cir_y) / 3
            y_down_ave = (y_max + y_min) / 2
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            #   输出最终数据
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        #   左侧定位点存在
        elif exit_flag == 1:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            #   画出位置，可注释
            cv.circle(img_gray, (int(x_min), int(y_min)), int(circle_min[0, :][0][2]), (0, 0, 0), 10)
            # 试剂点X轴方向误差
            dis_error = x_min - min_number
            print("试剂点X轴坐标误差值：", dis_error)
            #   输出X轴坐标
            point_x = self.__point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            y_arve_new = sum(cir_y) / 3
            y_down_ave = y_min
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            #   输出最终数据
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        #   右侧定位点存在
        elif exit_flag == 2:
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            #   画出位置，可注释
            cv.circle(img_gray, (int(x_max), int(y_max)), int(circle_max[0, :][0][2]), (0, 0, 0), 10)
            # 试剂点X轴方向误差
            dis_error = x_max - max_number
            print("试剂点X轴坐标误差值：", dis_error)
            #   输出X轴坐标
            point_x = self.__point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            y_arve_new = sum(cir_y) / 3
            y_down_ave = y_max
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            #   输出最终数据
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        #   底部定位点均不存在
        else:
            #   输出X轴坐标
            point_x = self.__point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            for i in range(8):
                point_y[i] = int(y_arve + point_y[i])
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y

    #   4.1 获取试剂点灰度值
    def img_get_gray(self, img_rota, gray_aver, nature_aver, circle_x, circle_y, point_x, point_y, dis_error, radius,
                     combina):
        #   获取试剂点的灰度值
        img_array = np.transpose(np.array(img_rota))
        print("定位点X轴：", circle_x)
        print("定位点X轴：", circle_y)
        #   获取定位点的灰度值
        for i in range(3):
            print("定位点:", i + 1, circle_x[i], circle_y[i])
            cv.circle(img_rota, (int(circle_x[i]), int(circle_y[i])), radius, (0, 0, 0), 10)
            gray_aver[0][i] = self.__sum_gray(img_array, int(circle_x[i]), int(circle_y[i]), radius)
        gray_aver[0][4] = gray_aver[0][2]
        gray_aver[0][2] = gray_aver[0][1]
        gray_aver[0][1] = 0
        #   获取试剂点的灰度值
        for i in range(5):
            for j in range(8):
                cv.circle(img_rota, (int(point_x[i] + j * (dis_error / 8)), point_y[j]), radius, (0, 0, 0), 10)
                gray_aver[j + 1][i] = self.__sum_gray(img_array, int(point_x[i] + j * (dis_error / 8)), point_y[j],
                                                      radius)
        #   获取灰度最小灰度值
        min_blackgrand_value = self.find_min_value(gray_aver)
        #   减去最小灰度值，变成规定的灰度值
        gray_aver = gray_aver - min_blackgrand_value
        #   输出各个试剂点的灰度值
        nature_aver = self.nature_positive_negative(gray_aver, nature_aver, combina)

        return gray_aver, nature_aver, img_rota, 1

    #   5 图像处理全流程
    def process(self, path_read, path_write, combina, radius):
        #   0 前期准备
        print("_______________________________________________")
        print("0    前期参数设置")
        #   开始时间
        start = time.perf_counter()
        #   参数设置
        gray_aver = np.zeros((9, 5), dtype=int)  # 输出参数
        nature_aver = np.zeros((9, 5), dtype=int)
        nature_aver = nature_aver.astype(str)
        #   获取图像
        img_ori = self.img_read(path_read)
        #   保存原始灰度图像
        cv.imwrite(path_write + 'img_0ori.jpeg', img_ori)
        self.img_resize(path_write + 'img_0ori.jpeg', path_write + "img_show_ori.jpeg")
        # cv.imwrite(path_write + 'img_final.jpeg', img_ori)
        #   获取环境的灰度值
        dst_init = self.__gray_round(img_ori)
        print("当前环境灰度值为：", self.gray_round)
        #   结束时间
        end = time.perf_counter()
        print("0    时间消耗：%.2f s" % (end - start))
        #   1 检测定位点
        print("_______________________________________________")
        print("1    获取区域内的定位点")
        #   开始时间
        start = time.perf_counter()
        num_flag = 0
        while True:
            num_flag += 1  # 循环次数
            dst_init -= 10  # 二值化初值
            self.gray_value = dst_init
            #   图像二值化
            img_dst = self.img_dst(img_ori, dst_init)
            #   图像膨胀
            img_dst = self.img_erosion(img_dst, 3)
            cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
            #   找出定位点位置
            judge, img_gray, circle, circle_x, circle_y = self.img_location_first(img_ori, img_dst, num=30, flag=0)
            if judge == 1:
                cv.imwrite(path_write + 'img_2ROI.jpeg', img_gray)
                print("检测到定位点，阈值为：", dst_init)
                break
            elif judge == 0:
                print("阈值为%03s" % dst_init + "\t" + "未检测到定位点")
            if num_flag >= 10:
                cv.imwrite(path_write + 'img_final.jpeg', img_ori)
                self.img_resize(path_write + 'img_final.jpeg', path_write + "img_show_final.jpeg")
                print("**错误：难以准确识别定位点")
                return 0, gray_aver, nature_aver
            else:
                continue

        #   结束时间
        end = time.perf_counter()
        print("1    时间消耗：%.2f s" % (end - start))
        #   2.3 矫正图像角度
        print("_______________________________________________")
        print("2    初次矫正图像角度")
        #   开始时间
        start = time.perf_counter()
        img_rota, img_rota_dst, middle_index = self.img_correct_first(img_ori, img_dst, circle_x, circle_y)
        #   结束时间
        end = time.perf_counter()
        print("2    时间消耗：%.2f s" % (end - start))

        print("_______________________________________________")
        print("3    再次矫正图像角度")
        #   开始时间
        start = time.perf_counter()
        point_x, point_y, dis_error, locat_x, locat_y = self.img_correct_second(img_rota, img_rota_dst, circle_x,
                                                                                circle_y, flag=1)
        #   结束时间
        end = time.perf_counter()
        print("3    时间消耗：%.2f s" % (end - start))

        print("_______________________________________________")
        print("4    圈定试剂点")
        #   开始时间
        start = time.perf_counter()
        gray_aver, nature_aver, img_rota, judge_1 = self.img_get_gray(img_rota, gray_aver, nature_aver, locat_x,
                                                                      locat_y, point_x, point_y, dis_error, radius,
                                                                      combina)

        font = cv.FONT_HERSHEY_SIMPLEX
        img_rota = cv.putText(img_rota, "Gray_Threshold: %s" % (self.gray_value), (50, 120), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "ROI_Down: %s" % (self.gray_down), (50, 250), font, 3, (255, 255, 255), 6)
        img_rota = cv.putText(img_rota, "Dip_Angle: %.3f" % (self.dip_angle), (50, 380), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "Gray_Surrounding: %.3f" % (self.gray_round), (50, 510), font, 3,
                              (255, 255, 255), 6)

        cv.imwrite(path_write + 'img_final.jpeg', img_rota)
        self.img_resize(path_write + 'img_final.jpeg', path_write + "img_show_final.jpeg")
        #   结束时间
        end = time.perf_counter()
        print("4    时间消耗：%.2f s" % (end - start))

        print(gray_aver)
        print(nature_aver)

        return 1, gray_aver, nature_aver


if __name__ == '__main__':
    imgPro = Image_Processing(
        roi_position=roi_position
    )

    #   开始时间
    # start = time.perf_counter()

    imgPro.process(path_read='D:\\WorkSpace\\VIDAS\\0pic_datasheet\\V2.0now\\1.jpeg',
                   path_write='./img_out/', combina="检测组合A", radius=40)
    #   结束时间
    # end = time.perf_counter()
    # print("0    图像获取——完成——初始化参数  时间消耗：%.2f s" % (end - start))
