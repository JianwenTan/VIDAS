import random
import datetime
import numpy as np
import serial
import serial.tools.list_ports

mixture20_A = [['', '', '', '', ''],
               ['榆树    ', '', '猫上皮  ', '', '葎草    '],
               ['', '花生    ', '', '蟹      ', ''],
               ['鸡蛋    ', '', '开/榛   ', '', '西红柿  '],
               ['', '悬铃木  ', '', '大豆    ', ''],
               ['小麦    ', '', '普通豚草', '', '鳕鱼    '],
               ['', '点/烟/交', '', '狗上皮  ', ''],
               ['蟑螂    ', '', '虾      ', '', '牛奶    '],
               ['', '屋/粉   ', '', '艾蒿    ', '']]

mixture20_B = [['', '', '', '', ''],
               ['黄/果/黑', '', '猫上皮  ', '', '苦艾    '],
               ['', '花生    ', '', '分/毛/根', ''],
               ['蛋清    ', '', '棉絮    ', '', '烟草屑  '],
               ['', '杨/柳   ', '', '大豆    ', ''],
               ['蜜蜂毒  ', '', '普通豚草', '', '蒲公英  '],
               ['', '交链孢霉', '', '狗上皮  ', ''],
               ['柏树    ', '', '蚊子唾液', '', '牛奶    '],
               ['', '屋尘螨  ', '', '艾蒿    ', '']]

mixture20_C = [['', '', '', '', ''],
               ['点/分/烟', '', '猫上皮  ', '', '葎草    '],
               ['', '花生    ', '', '蟹      ', ''],
               ['鸡蛋    ', '', '普通豚草', '', '鳕/龙/扇'],
               ['', '柳/杨/榆', '', '大豆    ', ''],
               ['羊肉    ', '', '虾      ', '', '屋尘    '],
               ['', '牛肉    ', '', '狗上皮  ', ''],
               ['蟑螂    ', '', 'CCD     ', '', '牛奶    '],
               ['', '屋/粉   ', '', '艾蒿    ', '']]

mixture13_D = [['', '', '', '', ''],
               ['', '鳕/鲑/鲈', '', '', ''],
               ['点/烟/分', '', '猫/狗   ', '', '总IgE   '],
               ['', '柏/榆/悬', '', '', ''],
               ['鸡蛋    ', '', '普/艾/苦', '', ''],
               ['', '牛/羊   ', '', '虾/蟹/扇', ''],
               ['花/开/腰', '', '屋尘    ', '', ''],
               ['', '屋/粉   ', '', '芒/菠/苹', ''],
               ['', '', '牛奶    ', '', '']]

result = [
    ' - ', ' + ', '++ ', '+++'
]

out = ['0'] * 100


# 阴性：F(x) = 0.000005833333333333333*x
# 弱阳性：F(x) = 0.0000052500000000000006*x+0.03499999999999996
# 中阳性：F(x) = 0.00003181818181818182*x-17.5
# 强阳性：
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
        self.ser = serial.Serial("COM14", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值

    def em5822_show(self, data):
        print(2)

    def em5822_instruction(self, data):
        print(3)

    def data_conversion(self, Base, Naturen, Light):
        #   过敏原设置
        sensi_arr = []
        #   性质标志
        Nat_Flag = np.zeros((9, 5), dtype=int)
        Nat_Flag = Nat_Flag.astype(str)
        #   过敏原浓度参考值
        Refer_value = np.zeros((9, 5), dtype=float)
        Refer_value = Refer_value.astype(str)
        # print(Refer_value)
        if Base[4] == "检测组合A":
            sensi_arr = mixture20_A
        elif Base[4] == "检测组合B":
            sensi_arr = mixture20_B
        elif Base[4] == "检测组合C":
            sensi_arr = mixture20_C
        elif Base[4] == "检测组合D":
            sensi_arr = mixture13_D
        #   计算过敏原性质-标志，计算过敏原浓度参考值
        for i in range(len(Naturen)):
            for j in range(len(Naturen[0])):
                if Naturen[i][j] == "阴性":
                    Nat_Flag[i][j] = result[0]
                    Naturen[i][j] = "阴性"
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "弱阳性":
                    Nat_Flag[i][j] = result[1]
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "中阳性":
                    Nat_Flag[i][j] = result[2]
                    Refer_value[i][j] = "<0.35"
                elif Naturen[i][j] == "强阳性":
                    Nat_Flag[i][j] = result[3]
                    Refer_value[i][j] = "<0.35"
                else:
                    Nat_Flag[i][j] = 0
                    Refer_value[i][j] = 0
        # print(Refer_value)

        return sensi_arr, Nat_Flag, Naturen, Refer_value

    def em5822_print(self, Base, Nature, Data_Light):
        sensi_arr = []
        Nat_Flag = []
        Light = []
        num = 0
        Data_Light = np.delete(Data_Light, 0, axis=0)
        sensi_arr, Nat_Flag, Nature, Light = self.data_conversion(Base, Nature, Data_Light)
        # print(sensi_arr, Nat_Flag)
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
                # print(num, row, column)
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

        for i in range(7 + num + 12):
            print_flag = 2
            if print_flag == 0:
                if i >= 6 and i <= 27:
                    continue
            elif print_flag == 1:
                if (i < 6) or (i > 10 and i < 7 + num + 12 - 2):
                    continue
            # print(out[i])
            self.ser.write(out[i].encode("GBK"))


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
    eprint = Em5822_Print()

    eprint.em5822_print(Data_Base, Data_Nature, Data_Light)
