import sys
from PIL import Image
import os
import datetime
import time

import gxipy as gx
import serial
import serial.tools.list_ports


class Image_Acquire:

    def __init__(self, path_cache, path_save):
        self.pathCa = path_cache
        self.pathSa = path_save
        Width_max = 5496
        Height_max = 3672
        self.Width_set = 1368  
        self.Height_set = 1150  
        self.OffsetX_set = [0, self.Width_set, self.Width_set * 2, self.Width_set * 3]
        self.OffsetY_set = [400, self.Height_set + 400]
        self.img_path = [self.pathCa + 'img0.jpeg', self.pathCa + 'img1.jpeg',
                         self.pathCa + 'img2.jpeg', self.pathCa + 'img3.jpeg',
                         self.pathCa + 'img4.jpeg', self.pathCa + 'img5.jpeg',
                         self.pathCa + 'img6.jpeg', self.pathCa + 'img7.jpeg']

        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            pass
        else:
            pass
            for comport in ports_list:
                pass
        self.ser = serial.Serial("/dev/ttyUSB1", 9600)  

    def __clear_cache(self):
        for i in os.listdir(self.pathCa):
            os.remove(self.pathCa + "%s" % i)
        pass

    def __img_check(self):
        if len(os.listdir(self.pathCa)) == 8:
            pass
            return 1
        else:
            return 0

    def img_cache(self):
        self.__clear_cache()
        flag = 0
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            sys.exit(1)
        strSN = dev_info_list[0].get("sn")
        cam = device_manager.open_device_by_sn(strSN)
        cam.Width.set(self.Width_set)
        cam.Height.set(self.Height_set)
        cam.ExposureTime.set(60000.0)
        while (True):
            cam.OffsetX.set(self.OffsetX_set[flag % 4])
            cam.OffsetY.set(self.OffsetY_set[flag // 4])
            write_len = self.ser.write("$810001D".encode('utf-8'))
            cam.stream_on()
            raw_img = cam.data_stream[0].get_image(timeout=10000)
            write_len = self.ser.write("$810011C".encode('utf-8'))
            cam.stream_off()
            RGB_img = raw_img.convert("RGB")
            if RGB_img is None:
                continue
            pass
            numpy_img = RGB_img.get_numpy_array()
            if numpy_img is None:
                continue
            pass
            img = Image.fromarray(numpy_img, "RGB")
            img.save(self.pathCa + "img%s.jpeg" % flag)
            flag += 1
            pass
            if flag == 8 and self.__img_check():
                cam.close_device()
                write_len = self.ser.write("$810011C".encode('utf-8'))
                break
            elif flag > 8:
                write_len = self.ser.write("$810011C".encode('utf-8'))
                flag = 0

    def img_merge(self, name):
        img = Image.open(self.img_path[0])
        width, height = img.size
        target_shape = (4 * width, 2 * height)
        target_shape_new = (4 * width, 4 * width)
        background = Image.new('L', target_shape)
        background_new = Image.new('L', target_shape_new)
        for i, img_num in enumerate(self.img_path):
            image = Image.open(img_num)
            image = image.resize((width, height))
            row, col = i // 4, i % 4
            location = (col * width, row * height)
            background.paste(image, location)
            background_new.paste(background, (0, 0))
        background_new.save(self.pathSa + "%s.jpeg" % name)
        img.close()
        self.__clear_cache()

    def serial_init(self):
        write_len = self.ser.write("$4100011".encode('utf-8'))
        data = self.ser.read_all()
        pass

    def camera_init(self):
        pass

    def img_acquire(self, name):
        self.img_cache()
        self.img_merge(name)


if __name__ == '__main__':
    path = "./img_test/"
    now = datetime.datetime.now()
    time_now = now.strftime("%Y_%m_%d_%H_%M_%S")

    start_time = time.perf_counter()

    imgAcq = Image_Acquire(path_cache="./img_cache/", path_save=path)

    imgAcq.img_acquire(name=time_now)

    end_time = time.perf_counter()
    pass
