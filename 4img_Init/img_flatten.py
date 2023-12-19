import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("D:\\WorkSpace\\VIDAS\\0pic_datasheet\\V2.1overexposure\\15.jpeg", 0)
# hist, bins = np.histogram(img.flatten(), 256, [0, 256])

plt.figure(figsize=(15, 15))
plt.subplot(131)
plt.title('gamma = 1')
plt.imshow(img, cmap='gray')  # 原图


# 默认gamma值为1.0，默认不变化
def adjust_gamma(image, gamma=1.0):
    invgamma = 1 / gamma
    brighter_image = np.array(np.power((image / 255), invgamma) * 255, dtype=np.uint8)
    return brighter_image


# gamma大于1，变亮
i = 0.35
img_gamma = adjust_gamma(img, gamma=i)
plt.subplot(132)
plt.title('gamma = %s' % i)
plt.imshow(img_gamma, cmap="gray")

# gamma小于1，变暗
i = 0.5
img_gamma = adjust_gamma(img, gamma=i)
plt.subplot(133)
plt.title('gamma = %s' % i)
plt.imshow(img_gamma, cmap="gray")

plt.show()
