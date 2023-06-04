import cv2
import pyscreeze
from screeninfo import get_monitors
import numpy as np

# 获取第二个显示器的大小和位置
monitors = get_monitors()
if len(monitors) > 1:
    monitor2 = monitors[0]
    width = monitor2.width
    height = monitor2.height
    x = monitor2.x
    y = monitor2.y

while True:
    # 捕获屏幕图像
    screenshot = pyscreeze.screenshot(region=(x, y, width, height))
    if screenshot is not None:
        # 将图像转换为字节字符串
        bytes_screenshot = screenshot.tobytes()
        # 使用OpenCV和Numpy读取图像
        image = np.frombuffer(bytes_screenshot, dtype=np.uint8)
        image = image.reshape(screenshot.size[1], screenshot.size[0], 3)
        image = cv2.resize(image,(640,480))
        cv2.imshow('Screen', image)
    # 按下 'q' 键退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
