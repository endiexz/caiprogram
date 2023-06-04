# author：chouti
import sys
from pathlib import Path
import cv2
import torch
import numpy
import time
import multiprocessing as mlp
from models.experimental import attempt_load
from utils.general import is_ascii, non_max_suppression, set_logging
from utils.torch_utils import select_device ,smart_inference_mode
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path
ROOT = FILE.parents[0]  # YOLOv5 root directory
#记录手机存在的时间
T1=time.process_time()
T11=time.process_time()
#记录两次手机出现之间的间隔
T2=time.process_time()
T21=T2+4000000
Phone_have=False
phone_have_log=False
phone_have_log_former=False
phone_location=[]
#手机是否出现事件检测
def phone_detect(List):
    global T1,T11,T2,T21,Phone_have,phone_location
    p_lose=3  #两次手机消失事件间隔
    p_have=3  #手机连续存在事件超过3秒判断存在
    if List[0] !=0:
        Phone_have=False
        for i in range(List[0]):
            if List[i+1][1] == 'cell phone':
                Phone_have=True
                phone_location=List[i+1][2]    #检测到的第一个手机的位置
                break
    if Phone_have:
        T2=T21
        T21=time.time()
    else:
        T21=time.time()
    if (T21-T2)>p_lose:
        T11=time.time()
        T1=T11
    else:
        T11=time.time()
    if (T11-T1)>60:
        T1=T11-50
    if (T21-T2)>60:
        T2=T21-40
    #print('lost is %.3f\n' % (T21 - T2))
    #print('exit is %.3f\n' % (T11 - T1))
    #手机出现时
    if (T11-T1)>p_have:
        #print('have')
        return True
    #手机消失时
    else:
        #print ("no")
        return False
    
@torch.no_grad()
def run(
        vq:mlp.Queue,  #video 里面获取图片进行检测
        yq:mlp.Queue,  #yolo 检测结果（物品的种类，数量）返回给show
        Key:mlp.Queue, #key (全局)
        material:mlp.Queue,  #（物品的种类）返回给show进行展示
        phone_state:mlp.Queue, #手机的状态返回给动画进行操作

        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        weights='yolov5--weights/yolov5s.pt',  # model.pt path(s)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        line_thickness=3,  # bounding box thickness (pixels)
        half=False,  # use FP16 half-precision inference
        dnn=False
        ):
    #手机状态检测的几个参数
    global phone_have_log,phone_have_log_former,phone_location
    # Initialize
    #yolo检测设备是否进行GPU加速或者cpu
    set_logging()
    device = select_device(device)
    print(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)  # load FP32 model
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    ascii = is_ascii(names)  # names are ascii (use PIL for UTF-8)
    #建立窗口（后面没有展示）
    capture = cv2.VideoCapture(0)

    while True:
        # 获取一帧 从vq video进程传递过来的
        #ret, frame = capture.read()
        #print('1')
        #队列空等待图片
        while vq.qsize()==0:
            time.sleep(0.001)
        num=(vq.qsize())-2
        #处理图片的最后两帧 之前的帧出队丢弃
        if num>0:
            for i in range(num):
                frame=vq.get()
        frame=vq.get()

        #yolo图片处理
        img = torch.from_numpy(frame).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        img = img.transpose(2, 3)
        img = img.transpose(1, 2)

        # Inference
        pred = model(img, augment=False, visualize=False)[0]

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Process predictions
        for i, det in enumerate(pred):  # detections per image
            #print(det)
            s = ''
            List=[]  #列表结构体存储检测到的种类数量以及坐标
            num=0 #积累检测物品的种类数
            annotator = Annotator(frame, line_width=line_thickness, pil=not ascii)
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                #print("shape:",det.shape)  #shape: torch.Size([1, 6]) 是一个二维的列表
                # Print results


                #从scale_boxes 类里面得到物品的种类数量等信息 并安排数据为一个新的list然后传递给video
                for c in det[:, -1].unique():  #remove the repetitve value
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += str(n.item()) + ' ' + str(names[int(c)]) + ' '  # add to string
                    list=[int(n.item()),str(names[int(c)])]
                    List.append(list)
                    num+=1

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = f'{names[c]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    #print(xyxy)
                    for i in range(num):
                        if str(names[c]) == List[i][1]:
                            List[i].append(annotator.P)
                    #print(annotator.P)
                    annotator.P=[]
                #将物品的数量插入到队首
                List.insert(0,num)
                #-----------------------
                #List 的结构
                #[num
                # [materialnum name [location]]
                # ............................
                # ............................
                # ............................
                # ]
                #传递手机的状态信息
                phone_have_log_former=phone_have_log
                phone_have_log=phone_detect(List)
                if phone_have_log_former ^ phone_have_log:
                    #print('-------------------------')
                    if phone_have_log:
                        phone_state.put(phone_location)
                        #print(phone_location)
                    else:
                        phone_state.put(False)
                #print(phone_state.qsize())
                #if not phone_state.empty():
                #    print(phone_state.get())



            if num!=0:
                yq.put(List)
                material.put(List)
            #print(material.qsize())
        if not Key.empty():
            break
    print('yoloquit')
    capture.release()
