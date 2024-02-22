# cython:language_level=3
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

import platform


#   运行函数
class Acq_Run:

    #   参数
    def __init__(self):
        #   初始化图像获取核心函数
        self.Core = Acq_Core()

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
            '../img/img_tem',
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
        #   获取主控类型
        Con_Flag = self.Core.system_pla()
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True and Con_Flag == True:
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
        if Con_Flag == True:
            #   调用需要保存日志的程序
            flag = self.Led_init()
        else:
            flag = True

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
        # 枚举设备。
        # dev_info_list 是设备信息列表，列表的元素个数为枚举到的设备个数，列表元素是字典，
        # 其中包含设备索引（index）、ip 信息（ip）等设备信息
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            return False
        else:
            return True
            # sys.exit(1)

    #   2 保存输出日志
    def Camera_init_log(self):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   获取主控类型
        Con_Flag = self.Core.system_pla()
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True and Con_Flag == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            Print_log = open("../log/log_CameraInit/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = Print_log
        else:
            pass

        #   判断主控系统类型
        if Con_Flag == True:
            #   调用需要保存日志的程序
            flag = self.Camera_init()
        else:
            flag = True

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    #   3 获取缓存图像
    def img_cache(self, path_chache):
        self.Core.clear_cache(path_chache)
        flag = 0
        # 枚举设备。
        # dev_info_list 是设备信息列表，列表的元素个数为枚举到的设备个数，列表元素是字典，
        # 其中包含设备索引（index）、ip 信息（ip）等设备信息
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            sys.exit(1)
        # 打开设备，获取设备基本信息列表
        strSN = dev_info_list[0].get("sn")
        # 通过序列号打开设备
        cam = device_manager.open_device_by_sn(strSN)
        # 配置摄像头
        cam.Width.set(self.Width_set)
        cam.Height.set(self.Height_set)
        cam.ExposureTime.set(60000.0)
        while (True):
            # 设置偏移值
            cam.OffsetX.set(self.OffsetX_set[flag % 4])
            cam.OffsetY.set(self.OffsetY_set[flag // 4])
            write_len = self.ser.write("$810001D".encode('utf-8'))
            # 开启采集
            cam.stream_on()
            # 获取一幅图像
            raw_img = cam.data_stream[0].get_image(timeout=10000)
            write_len = self.ser.write("$810011C".encode('utf-8'))
            cam.stream_off()
            # 图像转化
            RGB_img = raw_img.convert("RGB")
            if RGB_img is None:
                continue
            print(flag, '1成功')
            # 将图像数据创建numpy 数组
            numpy_img = RGB_img.get_numpy_array()
            if numpy_img is None:
                continue
            print(flag, '2成功')
            # 显示并保存图像
            img = Image.fromarray(numpy_img, "RGB")
            img.save(path_chache + "img%s.jpeg" % flag)
            flag += 1
            print(flag, '3成功')
            if flag == 8 and self.Core.img_check(path_chache):
                cam.close_device()
                write_len = self.ser.write("$810011C".encode('utf-8'))
                break
            elif flag > 8:
                write_len = self.ser.write("$810011C".encode('utf-8'))
                flag = 0
        pass

    #   3 图像获取全流程
    def img_acquire(self, path_chache, path_save, name):
        self.img_cache(path_chache)
        self.Core.img_merge(path_chache, path_save, name)
        return True

    #   3 保存输出日志
    def img_acquire_log(self, path_chache, path_save, name):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   获取主控类型
        Con_Flag = self.Core.system_pla()
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True and Con_Flag == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            Print_log = open("../log/log_CameraInit/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = Print_log
        else:
            pass

        #   判断主控系统类型，是否执行程序
        if Con_Flag == True:
            #   调用需要保存日志的程序
            flag = self.img_acquire(path_chache, path_save, name)
        else:
            flag = True

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag


#   核心函数
class Acq_Core:

    #   参数
    def __init__(self):
        pass

    #   1 删除缓存图像
    def clear_cache(self, path_cache):
        for i in os.listdir(path_cache):
            os.remove(path_cache + "%s" % i)
        print("缓存图片全部删除")

    #   2 检测缓存图像
    def img_check(self, path_cache):
        if len(os.listdir(path_cache)) == 8:
            print("图片获取完毕")
            return 1
        else:
            return 0

    #   3 系统检测
    def system_pla(self):
        #   系统信息标注
        system_info = [
            ['Linux', 'aarch64'],  # 嵌入式主控
            ['Windows', 'AMD64'],  # Windows主机
            ['Linux', 'X86_64']  # Linux主机
        ]
        #   获取系统ID
        system_id = platform.system()
        #   获取CPU的ID
        machine_id = platform.machine()
        #   判定是否为嵌入式主控
        if system_id == system_info[0][0] and machine_id == system_info[0][1]:
            return True
        else:
            return False

    #   4 图像拼接工作
    def img_merge(self, path_cache, path_save, name):
        #   设置缓存图片路径
        self.img_path = [path_cache + 'img0.jpeg', path_cache + 'img1.jpeg',
                         path_cache + 'img2.jpeg', path_cache + 'img3.jpeg',
                         path_cache + 'img4.jpeg', path_cache + 'img5.jpeg',
                         path_cache + 'img6.jpeg', path_cache + 'img7.jpeg']
        # 获取首张图片
        img = Image.open(self.img_path[0])
        # 获取尺寸
        width, height = img.size
        # 九宫格设置
        target_shape = (4 * width, 2 * height)
        target_shape_new = (4 * width, 4 * width)
        # 创建画布
        background = Image.new('L', target_shape)
        background_new = Image.new('L', target_shape_new)
        # 图像拼接
        for i, img_num in enumerate(self.img_path):
            # 读取图像
            image = Image.open(img_num)
            # 改变为统一尺寸
            image = image.resize((width, height))
            #   设置行列
            row, col = i // 4, i % 4
            # 定位
            location = (col * width, row * height)
            # 放置
            background.paste(image, location)
            background_new.paste(background, (0, 0))
        # 保存图像
        background_new.save(path_save + "%s.jpeg" % name)
        img.close()
        self.clear_cache(path_cache)
        pass
