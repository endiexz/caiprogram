import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk#图像控件
import multiprocessing as mlp
#开启桌面监控log参数
global wmq_log
wmq_log = 0
#每次点击按钮后该（window_monitor_log）参数被压入数值然后改变wmq_log的状态是否开启监控窗口
def wmq_log_t(window_monitor_log:mlp.Queue):
    global wmq_log
    window_monitor_log.put(1)
    print(1)
    if wmq_log == 1:
        wmq_log = 0
    else:
        wmq_log = 1 
#进程住入口函数
def show(ss:mlp.Queue,    #show_in_show 获取video处理过后的图片
         Key:mlp.Queue,   #全局进程开关
         material:mlp.Queue,          #yolo检测物品的结果
         anchor_box_q:mlp.Queue,      #是否打开物品检测开关的按钮
         window_monitor_q:mlp.Queue,  #
         window_monitor_log:mlp.Queue #打开桌面检测开关参数
         ):
    global wmq_log
    #创建tk界面
    top = tk.Tk()
    top.title('视频窗口')
    top.geometry('750x600')
    #定义展示视频的长宽
    image_width = 640
    image_height = 480
    #绘制画布
    canvas = Canvas(top,bg = 'white',width = image_width,height = image_height )
    #botton的frame
    button_frame=tk.Frame(top)
    button_frame.pack(side='right',padx=15,pady=10,fill=tk.Y)

    #退出按钮创建
    exit_box=tk.Button(button_frame, text='exit')
    exit_box.pack()
    exit_box.config(command=lambda:Key.put(1))

    #边框按钮创建
    anchor_box = tk.Button(button_frame, text='anchor_box')
    anchor_box.pack()
    anchor_box.config(command=lambda:anchor_box_q.put(1))

    #监控按钮创建
    desk_montior = tk.Button(button_frame,text = "desk_montior")
    desk_montior.pack()
    desk_montior.config(command=lambda:wmq_log_t(window_monitor_log))
    #drink_box = tk.Button(button_frame, text='drunk_box')
    #drink_box.pack()
    #drink_box.config(command=)

    text1=tk.StringVar()
    text1.set('None')
    timelog=0
    s= ''
    tk.Label(top,
             bd=1,
             textvariable=text1,
             relief=tk.SUNKEN,
             anchor='sw',
             fg='black',
             ).pack(side='bottom',fill=tk.X) 
    canvas.place(x = 0,y = 0)
    #进程循环
    while True:
        #从ss(show_in_show) 里面获取图片
        while ss.empty():
            continue
        #从material 里面获取物品的信息拼接后进行展示
        if material.empty():
            #print('empty')
            timelog+=1
            if timelog>20:
                text1.set('None')
            else:
                text1.set(s)
        else:
            s= ''
            timelog=0
            list=material.get()
            for i in range(list[0]):
                s+=str(list[i+1][0])+' ' + list[i+1][1] + ' '
            text1.set(s)
            #获取图片
        frame=ss.get()
        #进行图像颜色空间转换
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        pilImage=Image.fromarray(cvimage)
        pic = ImageTk.PhotoImage(image=pilImage)
        #展示每一帧图片
        canvas.create_image(0,0,anchor = 'nw',image = pic)
        top.update()
        top.after(1)
        if not Key.empty():
            print("clock quit")
            break
    top.destroy()
    top.mainloop()