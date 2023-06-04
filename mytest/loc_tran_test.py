import numpy as np
import cv2
def per_tranceformation(img):
    l_u = [195, 14]
    r_u = [581, 21]
    l_d = [208, 326]
    r_d = [555, 326]
    width = 640
    height = 480
    pts3 = np.float32([l_u,r_u,l_d,r_d])
    pts4 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix_Q = cv2.getPerspectiveTransform(pts3,pts4)
    img_Q = cv2.warpPerspective(img,matrix_Q,(width,height))
    return img_Q

if __name__=="__main__":
    capture=cv2.VideoCapture(0)
    ret,img = capture.read()
    img = per_tranceformation(img)
    while(1):
        cv2.imshow("image", img)
        if cv2.waitKey(0)&0xFF==27:      #esc退出
            break
    cv2.destroyAllWindows()