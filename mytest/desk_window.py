import tkinter as tk
import clock_tk
import multiprocessing as mlp
import time
from screeninfo import get_monitors

def get_pic(i):
    if(i>=42):
        i=1
    i=str(i)
    img='./desk/' + i + '.png'
    return img
def desk_window(
                phone_state:mlp.Queue,
                G_Code_location:mlp.Queue,
                Move_time:mlp.Queue,
                ):
    x=0
    y=0
    monitors = get_monitors()
    if len(monitors) > 1:
        monitor2 = monitors[1]
        width = monitor2.width
        height = monitor2.height
        x += monitor2.x
        y += monitor2.y


    #桌面(移动范围)相机比例
    ratiox=2570/640      #810 x 3.175 = 2,571.75
    ratioy=1540/480      #485 x 3.175 = 1,539.875
    root = tk.Tk()
    root.title('desk_window')  
    root.geometry("3840x2160+"+str(x)+"+"+str(y))   #需要修改3840x2160
    canvas = tk.Canvas(root, width=3840, height=2160)
    canvas.pack()
    ##鸭子的初始位置
    cartoon_init_location=[(600+100)/ratiox,(400+100)/ratioy]   #188 x3.175 = 596.9   128 x 3.175 = 406.4
    cartoon_last_station=0  #0在家，1充电
    cartoon_last_location=[cartoon_init_location[0],cartoon_init_location[1]]
    cartoon_move=False
    i=1
    log=0
    while True:
        log=0
        if cartoon_move == False:
            while not phone_state.empty():
                temp=phone_state.get()
                #print(temp)
                log=1
        if log==0 and cartoon_move == False:         #没有接收到任何信号图片就呆在上次停止的位置
            x_pos = cartoon_last_location[0]*ratiox
            y_pos = cartoon_last_location[1]*ratioy
        elif log==1 and cartoon_move == False and cartoon_last_station==0 and temp!=False:
            t=0
            x2=(temp[0]+temp[2])/2
            y2=(temp[1]+temp[3])/2
            ##
            location=[x2,y2]
            #print(location)
            G_Code_location.put(location)
            while Move_time.empty():
                time.sleep(0.001)
            move_time=Move_time.get()
            move_time=int(move_time) 
            print(move_time)
            cartoon_move = True
        elif log==1 and cartoon_move == False and cartoon_last_station==1 and temp==False:
            t=0
            x2=cartoon_init_location[0]
            y2=cartoon_init_location[1]
            ##
            location=[x2,y2]
            G_Code_location.put(location)
            while Move_time.empty():
                time.sleep(0.001)
            move_time=Move_time.get()
            move_time=int(move_time) 
            print(move_time)
            #print(location)
            cartoon_move = True
        elif log==1 and cartoon_move == False and cartoon_last_station==1 and temp!=False:
            t=0
            
            x2=(temp[0]+temp[2])/2
            y2=(temp[1]+temp[3])/2
            ##
            location=[x2,y2]
            G_Code_location.put(location)
            while Move_time.empty():
                time.sleep(0.001)
            move_time=Move_time.get()
            move_time=int(move_time) 
            #print(move_time)
            cartoon_move = True
        if cartoon_move:      
            x_pos=(cartoon_last_location[0] + (x2-cartoon_last_location[0])*t/move_time)*ratiox
            y_pos=(cartoon_last_location[1] + (y2-cartoon_last_location[1])*t/move_time)*ratioy
            #print(t)
            if t==int(move_time):
                cartoon_move=False
                if cartoon_last_station==1:
                    cartoon_last_station=0
                else :cartoon_last_station=1
                cartoon_last_location=[x2,y2]
            t+=1
        canvas.delete("all")
        time.sleep(0.01)
        img=get_pic(i)
        photo = tk.PhotoImage(file=img)
        canvas.create_image((x_pos, y_pos), image=photo)
        #画线
        if cartoon_move:
            canvas.create_line(x_pos, y_pos,x2*ratiox , y2*ratiox, fill='red', dash=(10,5), width=5)
        i=i+1
        if (i >= 42):
            i = 1
        canvas.update()
        
        
