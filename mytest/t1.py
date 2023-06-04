import tkinter as tk
from screeninfo import get_monitors
import pyscreeze

root = tk.Tk()
displays = get_monitors()
print(displays)
# 获取第二个显示器的大小和位置
if len(displays) > 1:
    width = displays[1].width
    height = displays[1].height
    x = displays[1].x
    y = displays[1].y
for display in displays:
    print(display)
screenshot = pyscreeze.screenshot(region=(x, y, width, height))