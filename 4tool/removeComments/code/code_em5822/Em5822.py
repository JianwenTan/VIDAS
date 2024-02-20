import random
import datetime
import numpy as np
import serial
import serial.tools.list_ports
import os
import sys
import time

from data_matrix import Data_matrix

out = ['0'] * 100


class Em5822_out:
    def __init__(self):
        self.Data = Data_matrix()
        self.Com = ""
        self.ComRun_flag = False

        self.Print_Save = True

        pass
        createFloder_path = [
            '../log',
            '../log/log_em5822Init',
            '../log/log_em5822Run'
        ]
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                pass
            else:
                pass

    def em5822_init(self):
        self.ports_list = list(serial.tools.list_ports.comports())
        for comport in self.ports_list:
            if list(comport)[1][0:16] == "USB-SERIAL CH340" or list(comport)[1][0:10] == "USB Serial":
                self.Com = "%s" % comport[0]
                pass
            else:
                continue
        if self.Com != "":
            try:  
                self.ser = serial.Serial(self.Com, 9600)  
                self.ComRun_flag = True  
                pass
                return True
            except Exception as e:  
                pass
                pass
                return False
        else:  
            return False

    def em5822_init_log(self):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("../log/log_em5822Init/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.em5822_init()

        end = time.perf_counter()  
        pass

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def em5822_serial(self):
        if len(self.ports_list) <= 0:
            pass
        else:  
            pass
            for comport in self.ports_list:
                pass

    def data_conversion(self, Base, Naturen, Light):
        sensi_arr = []
        Nat_Flag = np.zeros((9, 5), dtype=int)
        Nat_Flag = Nat_Flag.astype(str)
        Refer_value = np.zeros((9, 5), dtype=float)
        Refer_value = Refer_value.astype(str)

        if Base[4] == "检测组合A":
            sensi_arr = self.Data.mixture_A
        elif Base[4] == "检测组合B":
            sensi_arr = self.Data.mixture_B
        elif Base[4] == "检测组合C":
            sensi_arr = self.Data.mixture_C
        elif Base[4] == "检测组合D":
            sensi_arr = self.Data.mixture_D

        for i in range(len(Naturen)):
            for j in range(len(Naturen[0])):
                if Naturen[i][j] == "阴性":
                    Nat_Flag[i][j] = self.Data.result[0]
                    Naturen[i][j] = "阴性"
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "弱阳性":
                    Nat_Flag[i][j] = self.Data.result[1]
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "中阳性":
                    Nat_Flag[i][j] = self.Data.result[2]
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "强阳性":
                    Nat_Flag[i][j] = self.Data.result[3]
                    Refer_value[i][j] = "<0.35"
                else:
                    Nat_Flag[i][j] = 0
                    Refer_value[i][j] = 0

        return sensi_arr, Nat_Flag, Naturen, Refer_value

    def em5822_out(self, Base, Nature, Data_Light):
        if self.ComRun_flag == False:
            return False
        sensi_arr = []  
        Nat_Flag = []  
        Light = []  
        num = 0  
        Data_Light = np.delete(Data_Light, 0, axis=0)
        sensi_arr, Nat_Flag, Nature, Light = self.data_conversion(Base, Nature, Data_Light)
        out[0] = "        过敏原检验报告单\r\n"  
        out[1] = "姓名：%s      性别:%s\r\n" % (Base[0], Base[1])
        out[2] = "样本号：%s\r\n" % Base[2]
        out[3] = "条码号：%s\r\n" % Base[3]
        out[4] = "样本类型：%s\r\n" % Base[4]
        out[5] = "测试时间：%s\r\n" % Base[5]
        out[6] = "--------------------------------"
        out[7] = "过敏原     结果  参考值 结果解释\r\n"
        for i in range(45):
            row = int(i / 5)  
            column = int(i % 5)  
            if sensi_arr[row][column] != "":
                num += 1
                out[7 + num] = "%02d%s  %s  %s   %03s\r\n" % (num, sensi_arr[row][column], Nat_Flag[row][column],
                                                              Light[row][column], Nature[row][column])
        out[7 + num + 1] = "————————————————"
        out[7 + num + 2] = "注：\r\n"
        out[7 + num + 3] = "'-'为阴性，<0.35IU/mL\r\n"
        out[7 + num + 4] = "'+'为弱阳性，0.35IU/mL-3.5IU/mL\r\n"
        out[7 + num + 5] = "'++'为中阳性，3.5IU/mL-17.5IU/mL\r\n"
        out[7 + num + 6] = "'+++'为强阳性，≥17.5IU/mL\r\n"
        out[7 + num + 7] = "--------------------------------"
        out[7 + num + 8] = "打印时间：%s\r\n" % Base[6]
        out[7 + num + 9] = "    此检疫报告只对此标本负责，请结合临床。\r\n"
        out[7 + num + 10] = "\r\n"
        out[7 + num + 11] = "\r\n"

        try:
            for i in range(7 + num + 12):
                Print_flag = 2  
                if Print_flag == 0:
                    if i >= 6 and i <= 27:
                        continue
                elif Print_flag == 1:
                    if (i < 6) or (i > 10 and i < 7 + num + 12 - 2):
                        continue
                pass
                self.ser.write(out[i].encode("GBK"))  
            pass
            return True
        except Exception as e:
            pass
            pass
            return False

    def em5822_out_log(self, Base, Nature, Data_Light):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("../log/log_em5822Run/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.em5822_out(Base, Nature, Data_Light)

        end = time.perf_counter()  
        pass

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag


if __name__ == '__main__':
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    Data_Base = ["路人甲", "男", "0123456789", "9876543210", "检测组合A", time_now, time_now]
    Data_Nature = [['0', '0', '强阳性', '0', '0'],
                   ['弱阳性', '弱阳性', '弱阳性', '阴性', '弱阳性'],
                   ['弱阳性', '弱阳性', '阴性', '阴性', '弱阳性'],
                   ['强阳性', '弱阳性', '中阳性', '弱阳性', '弱阳性'],
                   ['强阳性', '弱阳性', '中阳性', '弱阳性', '弱阳性'],
                   ['弱阳性', '中阳性', '弱阳性', '弱阳性', '阴性'],
                   ['阴性', '中阳性', '阴性', '阴性', '阴性'],
                   ['阴性', '阴性', '阴性', '阴性', '阴性'],
                   ['阴性', '阴性', '阴性', '阴性', '阴性']]
    Data_Light = [[1095533, -298002, 1365723, -298002, 1372170],
                  [92754, 66682, 68361, 55653, 98561],
                  [94383, 84880, 50138, 57907, 75579],
                  [1375053, 343235, 924575, 383978, 187809],
                  [1375053, 328488, 884595, 391545, 187892],
                  [88829, 1042217, 73020, 72565, 26640],
                  [34906, 1046234, 41228, 32066, 20377],
                  [12650, 53237, 10125, 8014, 5839],
                  [0, 9031, 6793, 2547, 3514]]
    ePrint = Em5822_out()
    ePrint.em5822_init_log()
    ePrint.em5822_out_log(Data_Base, Data_Nature, Data_Light)
