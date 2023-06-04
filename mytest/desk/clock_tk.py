import tkinter as tk
import time


def clock(root):
    # 设置字体和颜色
    font_time = ("Arial", 20)
    font_date = ("Arial", 10)
    color = "#333333"

    # 创建框架，用于组织日期和时间标签
    frame = tk.Frame(root)
    frame.pack(side="bottom", anchor="se",)

    # 创建日期标签
    date = tk.Label(frame, font=font_date, fg=color)
    date.pack(side="top")

    # 创建时钟标签
    clock = tk.Label(frame, font=font_time, fg=color)
    clock.pack(side="top")

    # 循环更新时间和日期
    while True:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")
        clock.config(text=current_time)
        date.config(text=current_date)
        root.update()
        time.sleep(1)



def clock_main():
    root = tk.Tk()
    root.geometry("300x100+1400+900")
    root.overrideredirect(True)
    root.attributes("-transparentcolor", "white")
    root.config(bg="white")
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.5)
    clock(root)
    root.mainloop()
if __name__ == '__main__':
    clock_main()