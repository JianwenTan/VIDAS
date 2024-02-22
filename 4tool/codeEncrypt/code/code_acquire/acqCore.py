# encoding: utf-8
import sys
from PIL import Image
import os
import platform

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
