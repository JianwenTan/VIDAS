# encoding: utf-8
import sys
from PIL import Image
import os
import datetime
import time
# import frozen as frozen

import gxipy as gx
import serial
import serial.tools.list_ports

from acqCore import Acq_Core


class Acq_Run:

    #   参数
    def __init__(self):
        #   初始化图像获取核心函数
        # self.Core = Acq_Core()

        # self.Core.system_pla()

        # #   图像缓存路径
        # self.pathCa = path_cache
        # #   图像存储路径
        # self.pathSa = path_save
        #   设置摄像头分辨率
        Width_max = 5496
        Height_max = 3672
        self.Width_set = 1368  # 5496/4 = 1374
        self.Height_set = 1150  # 2300/2 = 1150
        self.OffsetX_set = [0, self.Width_set, self.Width_set * 2, self.Width_set * 3]
        # self.OffsetY_set = [200, self.Height_set + 200]
        self.OffsetY_set = [400, self.Height_set + 400]

        #   串口号初始值
        self.Com = ""
        #   串口是否可用的标志
        self.ComRun_flag = False
        #   文件保存标志，True保存，False不保存
        self.Print_Save = True

        print("_______________________________________________")
        #   创建文件夹目录
        createFloder_path = [
            '../img',
            '../img/img_cache',
            '../log',
            '../log/log_LedInit',
            '../log/log_CameraInit',
            '../log/log_AcqRun'
        ]
        #   创建文件夹
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                print("%s文件夹已经创建成功！" % i)
            else:
                print("%s文件夹已存在！" % i)


    #   1 灯源控制器初始化
    def Led_init(self):
        #   获取所有的串口信息
        self.ports_list = list(serial.tools.list_ports.comports())
        #   遍历，寻找可以使用的串口
        for comport in self.ports_list:
            if list(comport)[1][0:11] == "USB2.0-Ser！":
                self.Com = "%s" % comport[0]
                print("串口%s可用！" % self.Com)
            else:
                continue
        #   找到串口，执行初始化程序
        if self.Com != "":
            try:  # 串口初始化
                self.ser = serial.Serial(self.Com, 9600)  # 打开串口，将波特率配置为9600，其余参数使用默认值
                self.ComRun_flag = True  # 串口可用标志为True
                print("串口初始化完成！")
                return True
            except Exception as e:  # 报错执行
                print("串口不可用！")
                print(e)
                return False
        else:  # 未找到串口
            return False

    #   1 保存输出日志
    def Led_init_log(self):
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
            Print_log = open("../log/log_LedInit/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = Print_log
        else:
            pass

        #   判断主控系统类型
        sads = Acq_Core()
        Con_Flag = sads.system_pla()
        # if Con_Flag == True:
        #     #   调用需要保存日志的程序
        flag = self.Led_init()
        # else:
        #     flag = False

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    #   2 摄像头初始化
    def Camera_init(self):
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        print(dev_num)
        if dev_num == 0:
            sys.exit(1)
        pass

    #   3 图像获取全流程
    def img_cache(self):
        pass

if __name__ == '__main__':
    asd = Acq_Run()
    tjw = asd.Led_init_log()
    print(tjw)
