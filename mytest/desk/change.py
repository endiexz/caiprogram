
import cv2
import numpy as np
import imutils
from imutils import contours
import math
import time
#逆时针旋转

def change():
    frame = cv2.imread(r'D:\Code\yolov5-master\yolov5-master\data\images\test.png')
    np.set_printoptions(threshold=np.inf)
    img = cv2.imread('D:\Code\yolov5-master\yolov5-master\desk\white_mask.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = cv2.minAreaRect(contours[0])  # rect为[(旋转中心x坐标，旋转中心y坐标)，(矩形长，矩形宽),旋转角度]
    box_origin = cv2.boxPoints(rect)  # box_origin为[(x0,y0),(x1,y1),(x2,y2),(x3,y3)]


    M = cv2.getRotationMatrix2D(rect[0], rect[2], 1)
    dst = cv2.warpAffine(frame, M, (2 * img.shape[0], 2 * img.shape[1]))


    def Nrotate(angle, valuex, valuey, pointx, pointy):
        angle = (angle / 180) * math.pi
        valuex = np.array(valuex)
        valuey = np.array(valuey)
        nRotatex = (valuex - pointx) * math.cos(angle) - (valuey - pointy) * math.sin(angle) + pointx
        nRotatey = (valuex - pointx) * math.sin(angle) + (valuey - pointy) * math.cos(angle) + pointy
        return (nRotatex, nRotatey)


    # 顺时针旋转
    def Srotate(angle, valuex, valuey, pointx, pointy):
        angle = (angle / 180) * math.pi
        valuex = np.array(valuex)
        valuey = np.array(valuey)
        sRotatex = (valuex - pointx) * math.cos(angle) + (valuey - pointy) * math.sin(angle) + pointx
        sRotatey = (valuey - pointy) * math.cos(angle) - (valuex - pointx) * math.sin(angle) + pointy
        return (sRotatex, sRotatey)


    # 将四个点做映射
    def rotatecordiate(angle, rectboxs, pointx, pointy):
        output = []
        for rectbox in rectboxs:
            if angle > 0:
                output.append(Srotate(angle, rectbox[0], rectbox[1], pointx, pointy))
            else:
                output.append(Nrotate(-angle, rectbox[0], rectbox[1], pointx, pointy))
        return output


    box = rotatecordiate(rect[2], box_origin, rect[0][0], rect[0][1])


    def imagecrop(image, box):
        xs = [x[1] for x in box]
        ys = [x[0] for x in box]
        cropimage = image[min(xs):max(xs), min(ys):max(ys)]
        trans_img = cv2.transpose(cropimage)
        new_img = cv2.flip(trans_img, 1)
        cv2.imwrite(r'D:\Code\yolov5-master\yolov5-master\data\images\test.png',new_img)
        return new_img




    imagecrop(dst, np.int0(box))

def location(x1,y1):
    a=(23,44)
    K=5.4
    x1=int(x1)
    y1=int(y1)
    x2=(x1-18)/K
    y2=(y1-31)/K
    print(x2,y2)
if __name__ == '__main__':
    change()
    location(50,60)