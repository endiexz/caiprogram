import tkinter as tk
import time
import multiprocessing as mlp
from screeninfo import get_monitors
#主进程入口
def clock_main(
                Key:mlp.Queue,
                battery_link:mlp.Queue,
                battery_status:mlp.Queue,
                battery_power:mlp.Queue,
               ):
    
### 获取显示器信息
    displays = get_monitors()
    print(len(displays))
    # 获取第二个显示器的大小和位置
    x=1400
    y=300
    if len(displays) > 1:
        width = displays[1].width
        height = displays[1].height
        x += displays[1].x
        y += displays[1].y

    root = tk.Tk()
    root.geometry("300x200+"+str(x)+"+"+str(y))     
    root.overrideredirect(True)
    #root.attributes("-transparentcolor", "white")
    root.config(bg="white")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.5)
    # 设置字体和颜色
    font_time = ("Arial", 20)
    font_date = ("Arial", 10)
    font_power = ("Arial", 10)
    color = "#333333"
 
 
 ###电池最后的状态
    last_power = '-'
    last_link = 0
    last_status = 0
    # 创建框架，用于组织日期和时间标签
    frame = tk.Frame(root)
    frame.pack(side="bottom", anchor="se",)

    # 创建日期标签
    date = tk.Label(frame, font=font_date, fg=color)
    date.pack(side="top")

    # 创建时钟标签
    clock = tk.Label(frame, font=font_time, fg=color)
    clock.pack(side="top")
    #手机电量
    power1 = tk.Label(frame,font=font_power,fg=color)
    power1.pack(side="left")

    # 循环更新时间和日期
    #进程的循环
    while True:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")


        #手机状态的处理以及输出
        if battery_link.empty() != True:
            last_link = battery_link.get()
        if battery_power.empty() != True:
            last_power = battery_power.get()
        if battery_status.empty() != True:
            last_status = battery_status.get()
        if last_link == 0:
            current_power1 = "unlink"
        else:
            current_power1= "power:"+last_power+"%"
            #print(last_status)
            if last_status == 1:
                current_power1+="⚡️"
        #每次循环更新消息
        clock.config(text=current_time)
        date.config(text=current_date)
        power1.config(text=current_power1)
        root.update()
        time.sleep(0.1)
        if not Key.empty():
            print("clock quit")
            break
    root.destroy()
    root.mainloop()