import cv2

img = cv2.imread("2-2.jpeg")
print(img.shape)
num = 7
for i in range(num):
    row = int(i % 2)
    cloum = int(i / 2)
    cropped = img[(1368 * cloum):(1368 * (cloum + 1)), (1150 * row):(1150 * (row + 1))]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imwrite("%s.jpeg" % i, cropped)
