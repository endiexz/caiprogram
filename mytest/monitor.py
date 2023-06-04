import cv2
import numpy as np
import pyscreeze
import time
import multiprocessing as mlp
from screeninfo import get_monitors
def window_monitor(
        window_monitor_q:mlp.Queue,
        window_monitor_log:mlp.Queue
):
    wmq_log = 0
    wmq_tran = 0
    # 获取第二个显示器的大小和位置
    monitors = get_monitors()
    if len(monitors) > 1:
        monitor2 = monitors[1]
        width = monitor2.width
        height = monitor2.height
        x = monitor2.x
        y = monitor2.y
    while True:
        if window_monitor_log.empty() !=True:
            window_monitor_log.get()
            if wmq_log == 0:
                wmq_log =1
            else:
                wmq_log =0
        if wmq_log == 1:
            if len(monitors) > 1:
                screenshot = pyscreeze.screenshot(region=(x, y, width, height))
            else:
                screenshot = pyscreeze.screenshot()
            # 将图像转换为字节字符串
            bytes_screenshot = screenshot.tobytes()
            # 使用OpenCV和Numpy读取图像
            image = np.frombuffer(bytes_screenshot, dtype=np.uint8)
            image = image.reshape(screenshot.size[1], screenshot.size[0], 3)
            #参数为监控界面的大小
            image = cv2.resize(image,(640,480))
            cv2.imshow('Screen', image)
            cv2.waitKey(1)
            #time.sleep(0.1)
            # 显示图像
        if wmq_log ==1 and wmq_tran==0:
            wmq_tran = 1
        if wmq_log ==0 and wmq_tran==1:
            wmq_tran = 0
            #out.release()
            cv2.destroyAllWindows()
        else:
            #out.release()
            time.sleep(0.1)
