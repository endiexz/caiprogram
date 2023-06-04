import cv2
import os

# 获取图片目录
dir_path = 'D:\Code\yolov5-master\yolov5-master\desk\ey\\'

# 遍历目录下所有图片
for filename in os.listdir(dir_path):
    # 忽略非图片文件
    if not filename.endswith('.jpg') and not filename.endswith('.jpeg') and not filename.endswith('.png'):
        continue

    # 打开图片
    image = cv2.imread(dir_path + filename)

    # 修改图片大小
    image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_CUBIC)

    # 保存图片
    cv2.imwrite(filename, image)