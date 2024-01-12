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
    #   参数设置
    def __init__(self):
        #   过敏原矩阵初始化
        self.Data = Data_matrix()
        #   串口号初始值
        self.Com = ""
        #   串口是否可用的标志
        self.ComRun_flag = False

        #   文件保存标志，True保存，False不保存
        self.Print_Save = True

        #   创建日志文件夹，初始化部分
        if not os.path.exists("./code_print/log_init"):
            os.makedirs("./code_print/log_init")
            print("./code_print/log_init文件夹已经创建成功！")
        else:
            print("./code_print/log_init文件夹已存在！")
        #   创建日志文件夹，运行部分
        if not os.path.exists("./code_print/log_run"):
            os.makedirs("./code_print/log_run")
            print("./code_print/log_run文件夹已经创建成功！")
        else:
            print("./code_print/log_run文件夹已存在！")

    #   0 Em5822热转印打印机初始化程序
    def em5822_init(self):
        #   获取所有的串口信息
        self.ports_list = list(serial.tools.list_ports.comports())
        #   遍历，寻找可以使用的串口
        for comport in self.ports_list:
            if list(comport)[1][0:16] == "USB-SERIAL CH340" or list(comport)[1][0:10] == "USB Serial":
                self.Com = "%s" % comport[0]
                print("串口%s可用！" % self.Com)
            else:
                continue
        #   找到串口，执行初始化程序
        if self.Com != "":
            try:  # 串口初始化
                self.ser = serial.Serial(self.Com, 9600)  # 打开串口，将波特率配置为9600，其余参数使用默认值
                self.ComRun_flag = True  # 串口可用标志为True
                print("串口初始化完成！")
                return True
            except Exception as e:  # 报错执行
                print("串口不可用！")
                print(e)
                return False
        else:  # 未找到串口
            return False

    #   0 保存输出日志
    def em5822_init_log(self):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            print_log = open("./code_print/log_init/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = print_log
        else:
            pass

        #   调用需要保存日志的程序
        flag = self.em5822_init()

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    #   1 查看Em5822串口上连接的接口
    def em5822_serial(self):
        #   串口数判断
        if len(self.ports_list) <= 0:
            print("无串口设备。")
        else:  # 输出扫描出的串口
            print("可用的串口设备如下：")
            for comport in self.ports_list:
                print(list(comport)[0], list(comport)[1])

    #   2 过敏原标识
    def data_conversion(self, Base, Naturen, Light):
        #   过敏原设置
        sensi_arr = []
        #   性质标志
        Nat_Flag = np.zeros((9, 5), dtype=int)
        Nat_Flag = Nat_Flag.astype(str)
        #   过敏原浓度参考值
        Refer_value = np.zeros((9, 5), dtype=float)
        Refer_value = Refer_value.astype(str)

        #   检测组合进行对应
        if Base[4] == "检测组合A":
            sensi_arr = self.Data.mixture_A
        elif Base[4] == "检测组合B":
            sensi_arr = self.Data.mixture_B
        elif Base[4] == "检测组合C":
            sensi_arr = self.Data.mixture_C
        elif Base[4] == "检测组合D":
            sensi_arr = self.Data.mixture_D

        #   计算过敏原性质-标志
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

    #   3 热转印打印
    def em5822_print(self, Base, Nature, Data_Light):
        #   串口不可用，直接退出
        if self.ComRun_flag == False:
            return False
        sensi_arr = []  # 过敏原设置
        Nat_Flag = []  # 过敏原标志设置
        Light = []  # 发光值设置
        num = 0  # 打印行数
        #   删除第一行发光值的数据
        Data_Light = np.delete(Data_Light, 0, axis=0)
        #   将过敏原和过敏原性质、标志相对应
        sensi_arr, Nat_Flag, Nature, Light = self.data_conversion(Base, Nature, Data_Light)
        #   整理需要Em5822打印的数据
        out[0] = "        过敏原检验报告单\r\n"  # 8个空
        out[1] = "姓名：%s      性别:%s\r\n" % (Base[0], Base[1])
        out[2] = "样本号：%s\r\n" % Base[2]
        out[3] = "条码号：%s\r\n" % Base[3]
        out[4] = "样本类型：%s\r\n" % Base[4]
        out[5] = "测试时间：%s\r\n" % Base[5]
        out[6] = "--------------------------------"
        out[7] = "过敏原     结果  参考值 结果解释\r\n"
        for i in range(45):
            row = int(i / 5)  # 行
            column = int(i % 5)  # 列
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

        #   打印整理的数据
        try:
            for i in range(7 + num + 12):
                print_flag = 2  # 标志0，打印数据两端；标志1，打印数组正中间；其余标志，全部打印
                if print_flag == 0:
                    if i >= 6 and i <= 27:
                        continue
                elif print_flag == 1:
                    if (i < 6) or (i > 10 and i < 7 + num + 12 - 2):
                        continue
                print(out[i])  # 输出
                self.ser.write(out[i].encode("GBK"))  # 开始打印
            print("成功完成打印工作！")
            return True
        except Exception as e:
            print(e)
            print("未完成打印工作！")
            return False

    #   3 保存输出日志
    def em5822_print_log(self, Base, Nature, Data_Light):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   判断输出到控制台，还是日志中
        if self.Print_Save == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            print_log = open("./code_print/log_run/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = print_log
        else:
            pass

        #   调用需要保存日志的程序
        flag = self.em5822_print(Base, Nature, Data_Light)

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag


if __name__ == '__main__':
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    #   姓名，性别，样本号，条码号，样本类型，测试时间，打印时间
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
    # print(len(Data_Nature))
    eprint = Em5822_out()
    eprint.em5822_init_log()
    eprint.em5822_print_log(Data_Base, Data_Nature, Data_Light)
