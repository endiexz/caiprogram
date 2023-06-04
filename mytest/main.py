import multiprocessing as mlp
import test
import cv2
import time
import Processctl as pcc
if __name__ == '__main__':
    #开启全部进程
    process=pcc.Process()
    process.video_start()
    process.yolo_start()
    process.clock_start()
    process.show_start()
    process.desk_window_start()
    process.G_Code_tran_start()
    process.battery_start()
    process.window_monitor_start()
    #获取key结束全部进程
    while process.Key.empty():
        time.sleep(0.1)
    process.Terminate()
    print('yes')
    