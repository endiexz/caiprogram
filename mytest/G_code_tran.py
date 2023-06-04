# 这是一个示例 Python 脚本。
import time
import serial
import multiprocessing as mlp
import math
def G_code_Tran(
        G_Code_location:mlp.Queue,
        Move_time:mlp.Queue,
        ## 默认值
        ## 速度设定 mm/min
        x_rate = 500,
        y_rate = 500,
        z_rate = 500,
        ## step/mm  
        x_step = 700,  
        y_step = 700,
        z_step = 100,
        ## 加速度设定
        x_accel = 10,
        y_accel = 10,
        z_accel = 10,
        F_rate = 6000, #  指定移动的速度mm/min
        S_accel = 500, #指定移动的加速的
        X_M_pixel=1,
        Y_M_pixel=1,
        G_X_init_local=0,
        G_Y_init_local=0,
        Cart_X_init_local=100.0,
        Cart_Y_init_local=100.0,
        ):
    ##初始化
    G_X_last_location=G_X_init_local
    G_Y_last_location=G_Y_init_local
    print(Cart_X_init_local)


    init_var = [x_rate,y_rate,z_rate,x_step,y_step, z_step,x_accel,y_accel,z_accel] 
    init_loc = [110,111,112,100,101,102,120,121,122]
    global com,com1
    com = ['G21\n', 'G90\n', 'G92 X0Y0\n', 'S1000\n', 'F2000\n', 'G0Z0\n', 'M5\n', 'G4\n' 'P0.2\n']
    com1 = ['M3S1000\n', 'G4 P0.2\n', 'M5\n', 'G4 P0.2\n', 'G0 X0Y0\n']
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)  # 打开COM3波特率115200 超时2秒   linux上是/dev/ttyUSB0
    ser.timeout = 40  # 读超时设置
    ser.writeTimeout = 2  # 写超时
    temp=ser.readline()
    temp=ser.readline()
    print(temp)
    for i in range(9):
        it = '$'+str(init_loc[i])+'='+str(init_var[i])+'\n'
        ser.write(str.encode(it))
        Return = ser.readline().decode('utf-8').strip()
    print("grbl init over")
    while True:
        time1=time.time()
        while G_Code_location.empty():
            time.sleep(0.01)
            time2=time.time()
            if time2-time1 > 0.8:
                time1=time.time()
                ser.write(str.encode("?\n"))
                Return = ser.readline().decode('utf-8').strip()
                ser.readline().decode('utf-8').strip()
                #print(Return)
        loca=G_Code_location.get()
        print(loca)
        x=loca[0]
        y=loca[1]
        x,y=location_change(x,y,X_M_pixel,Y_M_pixel,G_X_init_local,G_Y_init_local,Cart_X_init_local,Cart_Y_init_local,)

        move_time=math.sqrt(math.pow(x-G_X_last_location,2)+math.pow(y-G_Y_last_location,2))/(F_rate/60)*100  #运动时间单位为0.01S
        G_X_last_location=x
        G_Y_last_location=y
        Move_time.put(move_time)
        #print(move_time)
        line= 'G1 X'+str(x)+'Y'+str(y)+'F'+str(F_rate)+'S'+str(S_accel)+'\n'
        #print(line)
        cmd = line.encode()
        ser.write(cmd)
        data = ser.readline().decode('utf-8').strip()  # 读取返回数据 10s超时

#进行坐标转换
def location_change(x,
                    y,
                    X_M_pixel, #mm/pixel
                    Y_M_pixel,
                    G_X_init_local,
                    G_Y_init_local,
                    Cart_X_init_local,
                    Cart_Y_init_local,
                    ):
    ## ?
    G_x=x*X_M_pixel+G_X_init_local
    G_y=y*Y_M_pixel+G_Y_init_local
    if(G_x>4000):
        print('NONE_X')
        print(G_x)
    elif(G_y>4000):
        print('NONE_y')
    else: return G_x,G_y 