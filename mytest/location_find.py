import cv2
import numpy as np
import multiprocessing as mlp

#获取透视变换的四个角点并将检测结果保存在location.dat里面
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global XY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        print(x,y)
        XY.append([x,y])
        cv2.imshow("image", img)
def location_find(
        #xy:mlp.Queue,
        #exit_code:mlp.Queue
):
    #img=cv2.imread('./desk/1.png')
    global img, XY
    f=open('location.dat','w')
    XY = []
    capture=cv2.VideoCapture(0)
    ret,img = capture.read()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    while(1):
        cv2.imshow("image", img)
        key=cv2.waitKey(0)&0xFF
        if key==27:
            print(XY)
            for i in range(4):
                for j in range(2):
                    f.write(str(XY[i][j])+"\n")
            f.close
            break
    cv2.destroyAllWindows()
if __name__ == "__main__":
    location_find()