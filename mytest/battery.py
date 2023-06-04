import subprocess
import multiprocessing as mlp
import time
def phone_link():
    #windows中使用platform-tools-windows
    #linux中使用platform-tools-linux
    command = "./platform-tools-linux/adb"
    ip = "192.168.1.107"
    #command+="| grep -o -E connect"
    result = subprocess.run([command, "connect" ,ip], capture_output=True, text=True)
    log=result.stdout[0]
    if log == 'u':
        return 0
    else:
        return 1
    #使用greb 和adb获取电量的大小
    #返回值为电量的大小
def power_get():
    dumpsys_command = ["./platform-tools-linux/adb", "shell", "dumpsys", "battery"]
    grep_command = ["grep", "-o", "-E", "level: +[0-9]+"]
    num_command = ["grep", "-o", "-E", "[0-9]+"]
    dumpsys_result = subprocess.run(dumpsys_command, capture_output=True, text=True)
    grep_result = subprocess.run(grep_command, input=dumpsys_result.stdout, capture_output=True, text=True)
    num_result = subprocess.run(num_command, input=grep_result.stdout, capture_output=True, text=True)
    power=str(int(num_result.stdout))
    return power
    #获取电量的状态
    #返回值为1 表示正在充电
    #返回值为0 表示没有充电
def power_status_get():
    command = ["./platform-tools-linux/adb","shell", "dumpsys", "battery"]
    grep_command= ["grep","-o", "-E", "USB powered:\ (true|false)"]
    grep1_command = ["grep", "-o", "-E", "\ (true|false)"]
    result = subprocess.run(command, capture_output=True, text=True)
    result1 = subprocess.run(grep_command, input=result.stdout, capture_output=True, text=True)
    result2 = subprocess.run(grep1_command, input=result1.stdout, capture_output=True, text=True)
    if result2.stdout[1] == 't':  #表示正在充电
        return 1
    else:
        return 0
    #进程入口函数
    #参数为手机的连接状态
def battery(
        battery_link:mlp.Queue,
        battery_status:mlp.Queue,
        battery_power:mlp.Queue,
):
    #循环判断手机的各种状态并压入 battery_link battery_status battery_power 后进行处理
    while True:
        log = phone_link()
        if log == 1:  #如果链接成功
            battery_link.put(1)
            status = power_status_get()
            battery_status.put(status)
            power = power_get()
            battery_power.put(power)
        else:
            battery_link.put(0)
        time.sleep(0.2)