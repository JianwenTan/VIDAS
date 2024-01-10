import random
import datetime

import serial
import serial.tools.list_ports




class Em5822_Print:

    def __init__(self):
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            print("无串口设备。")
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])
        # self.ser = serial.Serial("/dev/ttyUSB0", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值
        # self.ser = serial.Serial("/dev/ttyUSB1", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值




if __name__ == '__main__':
    eprint = Em5822_Print()
