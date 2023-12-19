import cv2 as cv

img = cv.imread("D:\\WorkSpace\\VIDAS\\0pic_datasheet\\V2.0now\\1.jpeg")

while True:
    cv.imshow("1", img)
    # 按 q 键退出
    if cv.waitKey(1) & 0xFF == ord('q'):
        # print(img.shape)
        break
