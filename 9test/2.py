import numpy as np
from PIL import Image
import cv2 as cv

img = Image.open("2-1.jpeg")
# 获取尺寸
width, height = img.size
print(height)
# 创建画布
background = Image.new('L', (height, height))

length = int((5488-2300)/2)

background.paste(img, (length, 1))

# 保存图像

background.save("1.jpeg")

img_or = cv.imread("1.jpeg")

img = background.resize((350,350), Image.ANTIALIAS)

img.save("2.jpeg")

