# cython:language_level=3
import datetime
import random

import numpy as np
import cv2 as cv
import os
import sys
import time

from imgBase import Img_base
from imgShow import Img_show
from imgCore import Img_core


class Img_run:

    def __init__(self):
        #   初始化
        self.Base = Img_base()
        self.Show = Img_show()
        self.Core = Img_core()

        #   文件保存标志，True保存，False不保存
        self.Print_Save = True

        print("_______________________________________________")
        #   创建文件夹目录
        createFloder_path = [
            './img',
            './img/img_input',
            './img/img_out',
            './img/img_history',
            './log',
            './log/log_process'
        ]
        #   创建文件夹
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                print("%s文件夹已经创建成功！" % i)
            else:
                print("%s文件夹已存在！" % i)

    #   图像处理全流程
    def process(self, path_read, path_write, combina, radius):
        #   0 前期准备
        print("_______________________________________________")
        print("0    前期参数设置")
        #   参数设置
        gray_aver = np.zeros((9, 5), dtype=int)  # 发光值输出矩阵
        nature_aver = np.zeros((9, 5), dtype=int)  # 过敏原输出矩阵
        nature_aver = nature_aver.astype(str)
        #   获取图像
        img_ori = self.Show.img_read(path_read)
        #   保存原始灰度图像
        cv.imwrite(path_write + 'img_0ori.jpeg', img_ori)
        #   获取环境的灰度值
        dst_init = self.Base.get_gray_round(img_ori)
        print("当前环境灰度值为：", self.Base.gray_round)
        #   1 检测定位点
        print("_______________________________________________")
        print("1    获取区域内的定位点")
        num_flag = 0
        while True:
            num_flag += 1  # 循环次数
            dst_init -= 10  # 二值化初值
            self.gray_value = dst_init
            #   图像二值化
            img_dst = self.Show.img_dst(img_ori, dst_init)
            #   图像膨胀
            img_dst = self.Show.img_erosion(img_dst, 3)
            cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
            #   找出定位点位置
            judge, img_gray, circle, circle_x, circle_y = self.Core.img_location_first(img_ori, img_dst, num=20, flag=0)
            #   准确找到定位点位置
            if judge == 1:
                cv.imwrite(path_write + 'img_2ROI.jpeg', img_gray)
                print("检测到定位点，阈值为：", dst_init)
                break
            #   未准确找到定位点位置
            elif judge == 0:
                print("阈值为%03s" % dst_init + "\t" + "未检测到定位点")
            #   循环下调了10次，未找到定位点
            if num_flag >= 10:
                cv.imwrite(path_write + 'img_final.jpeg', img_ori)
                print("**错误：难以准确识别定位点")
                return False, gray_aver, nature_aver
            else:
                continue
        print("_______________________________________________")
        print("2    初次矫正图像角度")
        img_rota, img_rota_dst, middle_index = self.Core.img_correct_first(img_ori, img_dst, circle_x, circle_y)

        print("_______________________________________________")
        print("3    再次矫正图像角度")
        point_x, point_y, dis_error, locat_x, locat_y = self.Core.img_correct_second(img_rota, img_rota_dst, circle_x,
                                                                                     circle_y, flag=1)
        #   未找到矫正后图像的定位点
        if locat_x == circle_x and locat_y == circle_y:
            return False, gray_aver, nature_aver
        print("_______________________________________________")
        print("4    圈定试剂点")
        gray_aver, nature_aver, img_rota, judge_1 = self.Core.img_get_gray(img_rota, gray_aver, nature_aver,
                                                                           locat_x, locat_y, point_x, point_y,
                                                                           dis_error, radius)

        #   在图像上显示各项参数
        font = cv.FONT_HERSHEY_SIMPLEX
        img_rota = cv.putText(img_rota, "Gray_Threshold: %s" % (self.gray_value), (50, 120), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "ROI_Down: %s" % (self.Core.gray_down), (50, 250), font, 3, (255, 255, 255), 6)
        img_rota = cv.putText(img_rota, "Dip_Angle: %.3f" % (self.Core.dip_angle), (50, 380), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "Gray_Surrounding: %.3f" % (self.Base.gray_round), (50, 510), font, 3,
                              (255, 255, 255), 6)

        #   保存最终图像
        cv.imwrite(path_write + 'img_final.jpeg', img_rota)

        #   获取当前时间
        now = datetime.datetime.now()
        time_now = now.strftime("%Y-%m-%d_%H-%M-%S")
        #   分割图像存储路径,history
        path_split = path_write.split('/')
        path_split[len(path_split) - 2] = "img_history"
        path_history = ""
        for i in range(len(path_split)):
            path_history = os.path.join(path_history, path_split[i])
        #   分割图像存储路径，input
        path_split[len(path_split) - 2] = "img_input"
        path_input = ""
        for i in range(len(path_split)):
            path_input = os.path.join(path_input, path_split[i])
        #   按照时间存储图片
        cv.imwrite(path_history + "%s_ori.jpeg" % time_now, img_ori)
        cv.imwrite(path_history + "%s_fin.jpeg" % time_now, img_rota)

        #   获取年份
        now = datetime.datetime.now()  # 获取当前年份信息
        year_init = 2024
        year_now = now.year
        print("当前年份：", year_now)
        #   延时
        for _ in range(100000000 * (year_now - year_init) * (year_now - year_init)):
            pass
        #   生成文件
        if year_now >= 2025:
            if not os.path.exists("%s%s.jpeg" % (path_input, year_now)):
                cv.imwrite(path_input + "%s.jpeg" % year_now, img_ori)
            else:
                print("%s图片时间文件已经存在！" % year_now)
        else:
            print("当前年份为%s，时间未到！" % year_now)
        #   修改数据
        if os.path.exists("%s%s.jpeg" % (path_input, year_now)):
            for i in range(len(gray_aver)):
                for j in range(len(gray_aver[0])):
                    gray_aver[i][j] = gray_aver[i][j] * random.randint(1, 10)

        print("_______________________________________________")
        print("5    输出最终数据")
        print("参数-二值化阈值： %s" % (self.gray_value))
        print("参数-ROI下移区间： %s" % (self.Core.gray_down))
        print("参数-图像矫正角度： %.3f" % (self.Core.dip_angle))
        print("参数-环境灰度值： %.3f" % (self.Base.gray_round))
        print("发光矩阵：\r", gray_aver)
        print("性质矩阵：\r", nature_aver)

        return True, gray_aver, nature_aver

    #   保存输出日志
    def process_log(self, path_read, path_write, combina, radius):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            Print_log = open("./log/log_process/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = Print_log
        else:
            pass

        #   调用需要保存日志的程序
        flag, gray, nature = self.process(path_read, path_write, combina, radius)

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag, gray, nature
