# cython:language_level=3
import math
import operator
import numpy as np
import cv2 as cv

import imgBase


class Img_core:

    def __init__(self):
        self.Base = imgBase.Img_base()

        #   ROI下移数值
        self.gray_down = 0
        #   图片旋转角度
        self.dip_angle = 0

    #   1 初次获取定位点
    def img_location_first(self, img_gray, img_dst, num, flag):
        '''
        参数1 img_gray    --灰度图像
        参数2 img_dst     --二值化图像
        参数3 num         --ROI下移次数
        参数4 flag        --画ROI区间和定位点的标志
        返回1 定位点是否寻找到的标志，1找到，0未找到
        返回2 img_gray    --输出灰度图像
        返回3 circle      --霍夫圆检测输出值
        返回4 circle_x    --圆变换输出X轴的值
        返回5 circle_y    --圆变换输出Y轴的值
        '''
        # 参数设置
        num_down = 0  # 总下移量
        num_init = 500  # 初始下移量
        len_down = 50  # 单次下移量
        circle_x = []  # 圆心点X轴坐标集合
        circle_y = []  # 圆心点Y轴坐标集合
        circle_r = []  # 圆心点半径集合
        for i in range(num):
            num_down = len_down * i + num_init  # 总下移量
            #   获取ROI感兴趣区间
            img_ROI = img_dst[(self.Base.roiPos[0][0] + num_down):(self.Base.roiPos[0][1] + num_down),
                      self.Base.roiPos[1][0]:self.Base.roiPos[1][1]]

            #   霍夫圆变换，获取ROI区间圆形区域
            circle = cv.HoughCircles(img_ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
            #   当前ROI未找到定位点
            if circle is None:
                continue
            #   当前ROI找到定位点不足3个
            elif circle.shape[1] < 3:
                continue
            #   当前ROI找到全部定位点
            elif circle.shape[1] >= 3:
                #   定位点坐标+ROI定位区间
                for i in range(circle.shape[1]):
                    circle[0][i][0] = circle[0][i][0] + self.Base.roiPos[1][0]
                    circle[0][i][1] = circle[0][i][1] + self.Base.roiPos[0][0] + num_down
                #   定位点坐标划分为x，y
                for j in circle[0, :]:
                    circle_x.append(j[0])
                    circle_y.append(j[1])
                    circle_r.append(j[2])

                #   退出标志
                exit_flag = 0

                #  标志1：检测定位点Y轴，像素误差大于200
                circle_y_sort = sorted(circle_y, key=float)  # 从小到大排列定位点Y轴数组
                diff_x1 = np.diff(circle_y_sort)  # 计算定位点Y轴数据的差值
                for i in range(len(diff_x1)):  # 循环判断差值是否大于200pix，大于就退出
                    if diff_x1[i] > 200:
                        exit_flag = 1
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：Y轴像素误差大于200")
                    #   清空定位点数组
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                #   标志2：检测定位点X轴，像素误差小于630
                circle_x_sort = sorted(circle_x, key=float)  # 从小到大排列定位点X轴数组
                diff_x2 = np.diff(circle_x_sort)  # 计算定位点X轴数据的差值
                for i in range(len(diff_x2)):  # 循环判断差值是否小于630pix，小于就退出
                    if diff_x2[i] < 630:
                        exit_flag = 1
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：X轴像素误差小于630")
                    #   清空定位点数组
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                #   标志3：检测定位点的灰度值均值，灰度均值误差大于20
                if circle.shape[1] == 3:  # 判断定位点是否只有3个
                    gray_posi = np.zeros(1 * 3)  # 初始化1*3数组
                    img_array = np.transpose(np.array(img_gray))  # 将图像转换为灰度数组
                    #   循环获取3个定位点的灰度均值
                    for j in range(3):
                        gray_posi[j] = self.Base.sum_gray_ave(img_array,
                                                              int(circle_x[j]),
                                                              int(circle_y[j]),
                                                              int(circle_r[j]))
                    #   获取定位点灰度均值的极值
                    min_index, min_number = min(enumerate(gray_posi), key=operator.itemgetter(1))
                    max_index, max_number = max(enumerate(gray_posi), key=operator.itemgetter(1))
                    if (max_number - min_number) >= 20:  # 如果定位点灰度均值极值大于20，退出
                        exit_flag = 1
                else:
                    gray_posi = np.zeros(1 * circle.shape[1])
                    exit_flag = 1

                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：灰度均值不一致")
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
                        cv.rectangle(img_gray,
                                     pt1=(self.Base.roiPos[1][0], self.Base.roiPos[0][0] + num_down),
                                     pt2=(self.Base.roiPos[1][1], self.Base.roiPos[0][1] + num_down),
                                     color=(0, 0, 0),
                                     thickness=20)
                        for j in circle[0, :]:
                            cv.circle(img_gray, (int(j[0]), int(j[1])), int(j[2]), (0, 0, 0), 10)
                    return 1, img_gray, circle, circle_x, circle_y
        # 未找到定位点
        return 0, img_gray, 0, circle_x, circle_y

    #   2 矫正图像角度
    def img_correct_first(self, img_gray, img_dst, circle_x, circle_y):
        '''
        参数1 img_gray        --灰度图像输入
        参数2 img_dst         --二值化图像输入
        参数3 circle_x        --定位点X轴集合
        参数4 circle_y        --定位点Y轴集合
        返回1 img_rota        --旋转后灰度图像
        返回2 img_rota_dst    --旋转后二值化图像
        返回3 middle_index    --定位点中间值索引
        '''
        #   获取最小值、最大值和中间值的索引
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
        self.dip_angle = angle  # 获取图像旋转角度
        print("---------------------")
        print("定位点倾斜角度：", angle)
        #   旋转图像
        img_rota = self.Base.rotate_img(img_gray, angle)
        img_rota_dst = self.Base.rotate_img(img_dst, angle)

        return img_rota, img_rota_dst, middle_index

    #   3 验证定位点
    def img_correct_second(self, img_gray, img_dst, circle_x, circle_y, flag):
        '''
        参数1 img_gray    --输入灰度图像
        参数2 img_dst     --输入二值化图像
        参数3 circle_x    --输入定位点X轴值
        参数4 circle_y    --输入定位点Y轴值
        参数5 flag        --ROI和定位点圈的标志
        返回1 point_x     --输出试剂点X轴坐标
        返回2 point_y     --输出试剂点Y轴坐标
        返回3 dis_error   --验证点底部误差
        返回4 cir_out_x   --定位点X轴输出坐标
        返回5 cir_out_y   --定位点X轴输出坐标
        '''
        #   参数设置
        cir_x = []  # 定位点X轴坐标
        cir_out_x = []
        cir_y = []  # 定位点Y轴坐标
        cir_out_y = []
        cir_r = []
        exit_flag = 0  # 退出标志
        dis_error = 0  # 验证点底部误差
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
            point_x = self.Base.point_X(min_num, circle_x[middle_index], max_num)
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
        img_array = np.transpose(np.array(img_gray))  # 将灰度图像转换为灰度值矩阵
        for j in range(3):
            gray_posi[j] = self.Base.sum_gray_ave(img_array, int(cir_x[j]), int(cir_y[j]), int(cir_r[j]))
        gray_ave = int((sum(gray_posi) / 3) * 100) / 100 - 20
        print("定位点灰度均值判读阈值：", gray_ave)

        #   画图
        if flag == 1:
            for j in circle[0, :]:
                cv.circle(img_gray, (int(j[0]), int(j[1] + y_arve)), int(j[2]), (0, 0, 0), 10)
            cv.rectangle(img_gray, pt1=(0, (y_arve)), pt2=(2500, (y_arve + 200)), color=(0, 0, 0), thickness=20)

        #   X轴定位点，获取定位点的索引值
        min_index, min_number = min(enumerate(cir_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(cir_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i
        #   从小到大排序定位点的X轴位置和Y轴位置
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
            max_gray_aver = self.Base.sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
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
            min_gray_aver = self.Base.sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
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
            min_gray_aver = self.Base.sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
            max_gray_aver = self.Base.sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
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
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
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
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
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
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
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
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            #   输出Y轴坐标
            for i in range(8):
                point_y[i] = int(y_arve + point_y[i])
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y

    #   4 获取试剂点灰度值
    def img_get_gray(self, img_rota, gray_aver, nature_aver, circle_x, circle_y, point_x, point_y,
                     dis_error, radius):
        '''
        参数1 img_rota        --旋转后灰度图像
        参数2 gray_aver       --发光值矩阵
        参数3 nature_aver     --荧光点性质矩阵
        参数4 circle_x        --定位点X轴坐标
        参数5 circle_y        --定位点Y轴坐标
        参数6 point_x         --试剂点X轴坐标
        参数7 point_y         --试剂点Y轴坐标
        参数8 dis_error       --底部验证点误差
        参数9 radius          --试剂点获取区域半径
        返回1 gray_aver       --返回发光值矩阵
        返回2 nature_aver     --返回过敏原性质矩阵
        返回3 img_rota        --返回旋转后图像
        返回4 标志未用
        '''
        #   获取试剂点的灰度值
        img_array = np.transpose(np.array(img_rota))
        print("定位点X轴：", circle_x)
        print("定位点X轴：", circle_y)
        #   获取定位点的灰度值
        for i in range(3):
            print("定位点:", i + 1, circle_x[i], circle_y[i])  # 输出定位点坐标
            cv.circle(img_rota, (int(circle_x[i]), int(circle_y[i])), radius, (0, 0, 0), 10)
            gray_aver[0][i] = self.Base.sum_gray(img_array, int(circle_x[i]), int(circle_y[i]), radius)
        gray_aver[0][4] = gray_aver[0][2]
        gray_aver[0][2] = gray_aver[0][1]
        gray_aver[0][1] = 0
        #   获取试剂点的灰度值
        for i in range(5):
            for j in range(8):
                cv.circle(img_rota, (int(point_x[i] + j * (dis_error / 8)), point_y[j]), radius, (0, 0, 0), 10)
                gray_aver[j + 1][i] = self.Base.sum_gray(img_array, int(point_x[i] + j * (dis_error / 8)), point_y[j],
                                                         radius)  # 输出试剂点的发光值
        #   获取灰度最小灰度值
        min_blackgrand_value = self.Base.find_min_value(gray_aver)
        #   减去最小灰度值，变成规定的灰度值
        gray_aver = gray_aver - min_blackgrand_value
        #   输出各个试剂点的性质
        nature_aver = self.Base.nature_positive_negative(gray_aver, nature_aver)

        return gray_aver, nature_aver, img_rota, 1
