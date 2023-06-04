import cv2

import numpy as np

img = cv2.imread(r'D:\Code\yolov5-master\yolov5-master\data\images\test.png', 0)

ret, th = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,  cv2.CHAIN_APPROX_SIMPLE)

color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

img = cv2.drawContours(color_img, contours, 50, (255, 0, 0), 2)
print(list(contours))
# bitwise_not对二值图像取反

cv2.imshow('th_img', cv2.bitwise_not(th))

cv2.imshow('contours_img', img)

cv2.waitKey(0)

cv2.destroyAllWindows()
