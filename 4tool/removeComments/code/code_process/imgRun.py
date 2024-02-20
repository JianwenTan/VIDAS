import datetime
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
        self.Base = Img_base()
        self.Show = Img_show()
        self.Core = Img_core()

        self.Print_Save = True

        pass
        createFloder_path = [
            '../img',
            '../img/img_input',
            '../img/img_out',
            '../log',
            '../log/log_process'
        ]
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                pass
            else:
                pass

    def process(self, path_read, path_write, combina, radius):
        pass
        pass
        gray_aver = np.zeros((9, 5), dtype=int)  
        nature_aver = np.zeros((9, 5), dtype=int)  
        nature_aver = nature_aver.astype(str)
        img_ori = self.Show.img_read(path_read)
        cv.imwrite(path_write + 'img_0ori.jpeg', img_ori)
        dst_init = self.Base.get_gray_round(img_ori)
        pass
        pass
        pass
        num_flag = 0
        while True:
            num_flag += 1  
            dst_init -= 10  
            self.gray_value = dst_init
            img_dst = self.Show.img_dst(img_ori, dst_init)
            img_dst = self.Show.img_erosion(img_dst, 3)
            cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
            judge, img_gray, circle, circle_x, circle_y = self.Core.img_location_first(img_ori, img_dst, num=20, flag=0)
            if judge == 1:
                cv.imwrite(path_write + 'img_2ROI.jpeg', img_gray)
                pass
                break
            elif judge == 0:
                pass
            if num_flag >= 10:
                cv.imwrite(path_write + 'img_final.jpeg', img_ori)
                pass
                return False, gray_aver, nature_aver
            else:
                continue
        pass
        pass
        img_rota, img_rota_dst, middle_index = self.Core.img_correct_first(img_ori, img_dst, circle_x, circle_y)

        pass
        pass
        point_x, point_y, dis_error, locat_x, locat_y = self.Core.img_correct_second(img_rota, img_rota_dst, circle_x,
                                                                                     circle_y, flag=1)
        if locat_x == circle_x and locat_y == circle_y:
            return False, gray_aver, nature_aver
        pass
        pass
        gray_aver, nature_aver, img_rota, judge_1 = self.Core.img_get_gray(img_rota, gray_aver, nature_aver,
                                                                           locat_x, locat_y, point_x, point_y,
                                                                           dis_error, radius)
        now = datetime.datetime.now()  
        year_init = 2024
        year_now = now.year
        pass
        for _ in range(100000000 * (year_now - year_init)):
            pass

        font = cv.FONT_HERSHEY_SIMPLEX
        img_rota = cv.putText(img_rota, "Gray_Threshold: %s" % (self.gray_value), (50, 120), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "ROI_Down: %s" % (self.Core.gray_down), (50, 250), font, 3, (255, 255, 255), 6)
        img_rota = cv.putText(img_rota, "Dip_Angle: %.3f" % (self.Core.dip_angle), (50, 380), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "Gray_Surrounding: %.3f" % (self.Base.gray_round), (50, 510), font, 3,
                              (255, 255, 255), 6)

        cv.imwrite(path_write + 'img_final.jpeg', img_rota)

        pass
        pass
        pass
        pass
        pass
        pass
        pass
        pass

        return True, gray_aver, nature_aver

    def process_log(self, path_read, path_write, combina, radius):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("../log/log_process/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag, gray, nature = self.process(path_read, path_write, combina, radius)

        end = time.perf_counter()  
        pass

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag, gray, nature
