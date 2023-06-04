import multiprocessing as mlp
import main
import test
import Video
import clock_tk
import show
import desk_window
import G_code_tran
import monitor
import battery
#创建进程类管理全部进程
class Process:
    def __init__(self):
        #---通讯队列
        #---图片传输  video->yolo(detect)
        self.video_put=mlp.Queue(30000)
        #---yolo检测结果[检测得到的物品的类别种类数量]传输  
        #---yolo->video
        self.yolo_detect_return=mlp.Queue(30000)
        #---进程结束关键字   
        #---从show里面的按钮（exit）获取然后传递给main结束全部进程
        #---show->main
        self.Key=mlp.Queue(3)
        #---video里面获取处理好的图片传递给show进行展示
        #---video->show
        #---show_in_show(ss)
        self.show_in_show=mlp.Queue(100)
        #---从yolo里面获取检测到的物品在show里面最下方状态栏进行展示
        #---yolo->show
        self.material=mlp.Queue(100)
        #---是否对图片加上检测到的边框  从按钮获得
        #---show->video
        self.anchor_box_q=mlp.Queue(10)
        #---手机的状态（存在）（消失）传递给动画进行处理
        #---yolo->desk_video
        self.phone_state=mlp.Queue(100)
        #---电机要移动的位置，从动画（desk_window）获得像素位置传递给电机
        #---desk_window->G_code_tran
        self.G_code_location=mlp.Queue(10)
        #---电机运动的时间从G_code_tran获取传递给动画进行速度匹配
        #---G_code_tran->desk_window
        self.Move_time=mlp.Queue(10)
        self.xy=mlp.Queue(10)       #透视变换获得源图像的角点
        self.exit_code=mlp.Queue(10)  #透视变换退出码
        #---摄像头设备
        #---从battery获取传递给clock进行显示
        self.dev=0  #'http://192.168.1.100:4747/video'
        self.battery_link=mlp.Queue(10)    #电池连接状态
        self.battery_status=mlp.Queue(10)  #电量的状态
        self.battery_power=mlp.Queue(10)   #电量的大小
        self.window_monitor_q=mlp.Queue(100)  #桌面监视
        self.window_monitor_log=mlp.Queue(10)  
        #Gbal初始化参数
        ##Grbl definition setting
        self.x_rate = 500
        self.y_rate = 500
        self.z_rate = 500
        ## steps/mm
        self.x_step = 0.7
        self.y_step = 0.7
        self.z_step = 100
        ## 加速度设定
        self.x_accel = 10
        self.y_accel = 10
        self.z_accel = 10
        self.F_rate = 6000 #  指定移动的速度600mm每秒
        self.S_accel = 6000 #指定移动的加速的
        ##单位mm/pixel图片每一个像素对应几mm
        self.X_M_pixel=0.315   #1/3.175 = 0.315
        self.Y_M_pixel=0.315
        ##Grbl初始位置
        self.G_X_init_local=0
        self.G_Y_init_local=0
        ##卡通的初始位置
        self.Cart_X_init_local=100.0
        self.Cart_Y_init_local=100.0

        #进程创建
        self.video=mlp.Process(target=Video.video,
                               args=(self.dev, 
                                     self.video_put,
                                     self.yolo_detect_return,
                                     self.Key,
                                     self.show_in_show,
                                     self.anchor_box_q,
                                     )
                                )
        self.yolo=mlp.Process(target=test.run,
                              args=(self.video_put,
                                    self.yolo_detect_return,
                                    self.Key,
                                    self.material,
                                    self.phone_state,
                                    )
                                )
        self.clock=mlp.Process(target=clock_tk.clock_main,
                               args=(
                                    self.Key,
                                    self.battery_link,
                                    self.battery_status,
                                    self.battery_power,
                                     )
                                )
        self.show=mlp.Process(target=show.show,
                              args=(self.show_in_show,
                                    self.Key,
                                    self.material,
                                    self.anchor_box_q,
                                    self.window_monitor_q,
                                    self.window_monitor_log,
                                    )
                                )
        self.desk_window=mlp.Process(target=desk_window.desk_window,
                                     args=( self.phone_state,
                                            self.G_code_location,
                                            self.Move_time,
                                           )
                                )
        self.G_code_tran=mlp.Process(target=G_code_tran.G_code_Tran, 
                                     args=(
                                        self.G_code_location,
                                        self.Move_time,
                                        ## 速度设定 mm/min
                                        self.x_rate,
                                        self.y_rate,
                                        self.z_rate,
                                        ## 范围设定
                                        self.x_step,
                                        self.y_step,
                                        self.z_step,
                                        ## 加速度设定
                                        self.x_accel,
                                        self.y_accel,
                                        self.z_accel,
                                        self.F_rate, #  指定移动的速度
                                        self.S_accel, #指定移动的加速的
                                        self.X_M_pixel,
                                        self.Y_M_pixel,
                                        ##Grbl初始位置
                                        self.G_X_init_local,
                                        self.G_Y_init_local,

                                        self.Cart_X_init_local,
                                        self.Cart_Y_init_local,
                                     ))
        self.battery=mlp.Process(target=battery.battery,
                                 args=(
                                        self.battery_link,
                                        self.battery_status,
                                        self.battery_power,
                                 ))
        self.window_monitor=mlp.Process(target=monitor.window_monitor,
                                        args=(
                                        self.window_monitor_q,
                                        self.window_monitor_log,
                                        ))
    def video_start(self):
        self.video.start()
    def yolo_start(self):
        self.yolo.start()
    def clock_start(self):
        self.clock.start()
    def show_start(self):
        self.show.start()
    def desk_window_start(self):
        self.desk_window.start()
    def G_Code_tran_start(self):
        self.G_code_tran.start()
    def battery_start(self):
        self.battery.start()
    def window_monitor_start(self):
        self.window_monitor.start()
    def Join(self):
        self.video.join()
        self.yolo.join()
        self.clock.join()
    def Terminate(self):
        self.video.terminate()
        self.yolo.terminate()
        self.clock.terminate()
        self.show.terminate()
        self.desk_window.terminate()
        self.G_code_tran.terminate()
        self.battery.terminate()
        self.window_monitor.terminate()