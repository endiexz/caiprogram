import cv2
import main
import multiprocessing as mlp
import numpy as np
import threading
import queue

#防止网络视频阻塞处理
class VideoCapture:
    """Customized VideoCapture, always read latest frame"""

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue(maxsize=3)
        self.stop_threads = False  # to gracefully close sub-thread
        th = threading.Thread(target=self._reader)
        th.daemon = True
        th.start()

    # 实时读帧，只保存最后一帧
    def _reader(self):
        while not self.stop_threads:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def terminate(self):
        self.stop_threads = True
        self.cap.release()


#透视变换
#返回结果为处理过后的图片
def per_tranceformation(img,XY):
    width = 640
    height = 480
    pts3 = np.float32(XY)
    pts4 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix_Q = cv2.getPerspectiveTransform(pts3,pts4)
    img_Q = cv2.warpPerspective(img,matrix_Q,(width,height))
    return img_Q
#主进程入口函数
def video(dev,   #视频设备
          q:mlp.Queue,   #向yolo传递图片
          vq:mlp.Queue,  #获取yolo处理的结果
          Key:mlp.Queue, #全局key
          ss:mlp.Queue,  #将处理过后的图片传递给show
          anchor_box_q:mlp.Queue,  #是否加入检测结果边框
          color=(255, 0, 0),       #检测边框的颜色
          video_show=False,        #是否直接进行图片展示
          draw_in_video =False     #时候在video里面花边框初始值为否
          ):
    ## 图片裁剪
    copy_x=0
    copy_y=0
    copy_h=360
    copy_w=640
    XY = []


    #读取透视变换四个角点位置信息，从location.dat里面读取
    f=open('location.dat')
    for i in range(4):
        lx = f.readline().strip()
        ly = f.readline().strip()
        xy = [int(lx), int(ly)]
        XY.append(xy)
    print(XY)
    f.close

    #如果video_show为true则进行展示
    if video_show:
        cv2.namedWindow('video_w',cv2.WINDOW_NORMAL)   #创建窗口
        cv2.resizeWindow('video_w',640,480)  #设置窗口大小
    cap = VideoCapture(dev)
    #capture = cv2.VideoCapture(dev)

    #首先进行值的初始化防止出现变量未定义的情况
    logtime=0 #记录没有得到返回锚框时间
    list=None
    anchor_log=0
    #主进程循环
    while True:
        #获取图片
        pic = cap.read()
        pic=per_tranceformation(pic,XY)
        #pic = pic[copy_y:copy_y+copy_h, copy_x:copy_x+copy_w]
        #if not ret:
        #    break
        key = cv2.waitKey(1) 
        #向yolo传递图片
        q.put(pic)
        #是否进行花边框处理
        if not anchor_box_q.empty():
            anchor_box_q.get()
            if anchor_log==0:
                anchor_log=1
                draw_in_video=True
            else:
                anchor_log=0
                draw_in_video=False
        #如果draw_in_video 为true则花边框否则不进行处理
        if draw_in_video:
            if not vq.empty():
                logtime=0
                list=vq.get()
            else:
                if logtime <30:
                    logtime+=1
                else:list = None
            if logtime<30 and list !=None:
                for i in range(list[0]):
                    for j in range(list[i+1][0]):
                        cv2.rectangle(pic,(list[i+1][2+j][0],list[i+1][2+j][1]),(list[i+1][2+j][2],list[i+1][2+j][3]),color,2)
        else:
            if not vq.empty():
                list=vq.get()
            else:list = None
        
        #如果video_show为true则进行 实时展示，
        if video_show:
            cv2.imshow('video_w',pic)
        ss.put(pic)
        if key  == ord('q') or not Key.empty():
            Key.put(1)
            break
    print('video quit')
    cv2.destroyAllWindows()