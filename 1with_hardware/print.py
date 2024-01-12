import random
import datetime
import numpy as np
import serial
import serial.tools.list_ports

mixture20_A = [['榆树    ', '', '猫上皮  ', '', '葎草    '],
               ['', '花生    ', '', '蟹      ', ''],
               ['鸡蛋    ', '', '开/榛   ', '', '西红柿  '],
               ['', '悬铃木  ', '', '大豆    ', ''],
               ['小麦    ', '', '普通豚草', '', '鳕鱼    '],
               ['', '点/烟/交', '', '狗上皮  ', ''],
               ['蟑螂    ', '', '虾      ', '', '牛奶    '],
               ['', '屋/粉   ', '', '艾蒿    ', '']]

mixture20_B = [['黄/果/黑', '', '猫上皮  ', '', '苦艾    '],
               ['', '花生    ', '', '分/毛/根', ''],
               ['蛋清    ', '', '棉絮    ', '', '烟草屑  '],
               ['', '杨/柳   ', '', '大豆    ', ''],
               ['蜜蜂毒  ', '', '普通豚草', '', '蒲公英  '],
               ['', '交链孢霉', '', '狗上皮  ', ''],
               ['柏树    ', '', '蚊子唾液', '', '牛奶    '],
               ['', '屋尘螨  ', '', '艾蒿    ', '']]

mixture20_C = [['点/分/烟', '', '猫上皮  ', '', '葎草    '],
               ['', '花生    ', '', '蟹      ', ''],
               ['蛋清    ', '', '普通豚草', '', '鳕/龙/扇'],
               ['', '柳/杨/榆', '', '大豆    ', ''],
               ['羊肉    ', '', '虾      ', '', '屋尘    '],
               ['', '牛肉    ', '', '狗上皮  ', ''],
               ['蟑螂    ', '', 'CCD     ', '', '牛奶    '],
               ['', '屋/粉   ', '', '艾蒿    ', '']]

mixture13_D = [['', '鳕/鲑/鲈', '', '虾/蟹/扇', ''],
               ['点/烟/分', '', '猫/狗   ', '', ''],
               ['', '柏/榆/悬', '', '牛奶    ', ''],
               ['鸡蛋    ', '', '普/艾/苦', '', '总IgE   '],
               ['', '牛/羊   ', '', '芒/菠/苹', ''],
               ['花/开/腰', '', '屋尘    ', '', ''],
               ['', '屋/粉   ', '', '', ''],
               ['', '', '', '', '']]

result = [
    ' - ', ' + ', '++ ', '+++'
]

out = ['0'] * 39


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
        Nat_Flag = np.zeros((8, 5), dtype=int)
        Nat_Flag = Nat_Flag.astype(str)
        #   过敏原浓度参考值
        Refer_value = np.zeros((8, 5), dtype=float)
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
                    Naturen[i][j] = "  阴性"
                    Refer_value[i][j] = Light[i][j] * 0.000005833333333333333
                elif Naturen[i][j] == "弱阳性":
                    Nat_Flag[i][j] = result[1]
                    Refer_value[i][j] = Light[i][j] * 0.0000052500000000000006 + 0.03499999999999996
                elif Naturen[i][j] == "中阳性":
                    Nat_Flag[i][j] = result[2]
                    Refer_value[i][j] = Light[i][j] * 0.00003181818181818182 - 17.5
                elif Naturen[i][j] == "强阳性":
                    Nat_Flag[i][j] = result[3]
                    Refer_value[i][j] = Light[i][j] * 0.00003181818181818182 - 17.5
                else:
                    Nat_Flag[i][j] = 0
                    Refer_value[i][j] = 0
        print(Refer_value)

        if Base[4] == "检测组合D":
            for i in range(len(Naturen)):
                for j in range(len(Naturen[0])):
                    if j % 2 == 0 and i % 2 == 1:
                        sensi_arr[i - 1][j] = sensi_arr[i][j]
                        sensi_arr[i][j] = "0"
                        Naturen[i - 1][j] = Naturen[i][j]
                        Naturen[i][j] = "0"
                        Nat_Flag[i - 1][j] = Nat_Flag[i][j]
                        Nat_Flag[i][j] = "0"
                        Refer_value[i - 1][j] = Refer_value[i][j]
                        Refer_value[i][j] = "0"
                    if i % 2 == 0 and j % 2 == 1:
                        sensi_arr[i + 1][j] = sensi_arr[i][j]
                        sensi_arr[i][j] = "0"
                        Naturen[i + 1][j] = Naturen[i][j]
                        Naturen[i][j] = "0"
                        Nat_Flag[i + 1][j] = Nat_Flag[i][j]
                        Nat_Flag[i][j] = "0"
                        Refer_value[i + 1][j] = Refer_value[i][j]
                        Refer_value[i][j] = "0"

        return sensi_arr, Nat_Flag, Naturen, Refer_value

    def em5822_print(self, Base, Nature, Data_Light):
        sensi_arr = []
        Nat_Flag = []
        Light = []
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
        out[8] = "01%s  %s  %5.2f   %s\r\n" % (sensi_arr[0][0], Nat_Flag[0][0], Light[0][0], Nature[0][0])
        out[9] = "02%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][0], Nat_Flag[2][0], Light[2][0], Nature[2][0])
        out[10] = "03%s  %s  %5.2f   %s\r\n" % (sensi_arr[4][0], Nat_Flag[4][0], Light[4][0], Nature[4][0])
        out[11] = "04%s  %s  %5.2f   %s\r\n" % (sensi_arr[6][0], Nat_Flag[6][0], Light[6][0], Nature[6][0])
        out[12] = "05%s  %s  %5.2f   %s\r\n" % (sensi_arr[1][1], Nat_Flag[1][1], Light[1][1], Nature[1][1])
        out[13] = "06%s  %s  %5.2f   %s\r\n" % (sensi_arr[3][1], Nat_Flag[3][1], Light[3][1], Nature[3][1])
        out[14] = "07%s  %s  %5.2f   %s\r\n" % (sensi_arr[5][1], Nat_Flag[5][1], Light[5][1], Nature[5][1])
        out[15] = "08%s  %s  %5.2f   %s\r\n" % (sensi_arr[7][1], Nat_Flag[7][1], Light[7][1], Nature[7][1])
        out[16] = "09%s  %s  %5.2f   %s\r\n" % (sensi_arr[0][2], Nat_Flag[0][2], Light[0][2], Nature[0][2])
        out[17] = "10%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][2], Nat_Flag[2][2], Light[2][2], Nature[2][2])
        out[18] = "11%s  %s  %5.2f   %s\r\n" % (sensi_arr[4][2], Nat_Flag[4][2], Light[4][2], Nature[4][2])
        out[19] = "12%s  %s  %5.2f   %s\r\n" % (sensi_arr[6][2], Nat_Flag[6][2], Light[6][2], Nature[6][2])
        out[20] = "13%s  %s  %5.2f   %s\r\n" % (sensi_arr[1][3], Nat_Flag[1][3], Light[1][3], Nature[1][3])
        out[21] = "14%s  %s  %5.2f   %s\r\n" % (sensi_arr[3][3], Nat_Flag[3][3], Light[3][3], Nature[3][3])
        out[22] = "15%s  %s  %5.2f   %s\r\n" % (sensi_arr[5][3], Nat_Flag[5][3], Light[5][3], Nature[5][3])
        out[23] = "16%s  %s  %5.2f   %s\r\n" % (sensi_arr[7][3], Nat_Flag[7][3], Light[7][3], Nature[7][3])
        out[24] = "17%s  %s  %5.2f   %s\r\n" % (sensi_arr[0][4], Nat_Flag[0][4], Light[0][4], Nature[0][4])
        out[25] = "18%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][4], Nat_Flag[2][4], Light[2][4], Nature[2][4])
        out[26] = "19%s  %s  %5.2f   %s\r\n" % (sensi_arr[4][4], Nat_Flag[4][4], Light[4][4], Nature[4][4])
        out[27] = "20%s  %s  %5.2f   %s\r\n" % (sensi_arr[6][4], Nat_Flag[6][4], Light[6][4], Nature[6][4])
        out[28] = "————————————————"
        out[29] = "注：\r\n"
        out[30] = "'-'为阴性，<0.35IU/mL\r\n"
        out[31] = "'+'为弱阳性，0.35IU/mL-3.5IU/mL\r\n"
        out[32] = "'++'为中阳性，3.5IU/mL-17.5IU/mL\r\n"
        out[33] = "'+++'为强阳性，≥17.5IU/mL\r\n"
        out[34] = "--------------------------------"
        out[35] = "打印时间：%s\r\n" % Base[6]
        out[36] = "    此检疫报告只对此标本负责，请结合临床。\r\n"
        out[37] = "\r\n"
        out[38] = "\r\n"

        if Base[4] == "检测组合D":
            out[8] = "01%s  %s  %5.2f   %s\r\n" % (sensi_arr[0][0], Nat_Flag[0][0], Light[0][0], Nature[0][0])
            out[9] = "02%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][0], Nat_Flag[2][0], Light[2][0], Nature[2][0])
            out[10] = "03%s  %s  %5.2f   %s\r\n" % (sensi_arr[4][0], Nat_Flag[4][0], Light[4][0], Nature[4][0])
            out[11] = "04%s  %s  %5.2f   %s\r\n" % (sensi_arr[1][1], Nat_Flag[1][1], Light[1][1], Nature[1][1])
            out[12] = "05%s  %s  %5.2f   %s\r\n" % (sensi_arr[3][1], Nat_Flag[3][1], Light[3][1], Nature[3][1])
            out[13] = "06%s  %s  %5.2f   %s\r\n" % (sensi_arr[5][1], Nat_Flag[5][1], Light[5][1], Nature[5][1])
            out[14] = "07%s  %s  %5.2f   %s\r\n" % (sensi_arr[7][1], Nat_Flag[7][1], Light[7][1], Nature[7][1])
            out[15] = "08%s  %s  %5.2f   %s\r\n" % (sensi_arr[0][2], Nat_Flag[0][2], Light[0][2], Nature[0][2])
            out[16] = "09%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][2], Nat_Flag[2][2], Light[2][2], Nature[2][2])
            out[17] = "10%s  %s  %5.2f   %s\r\n" % (sensi_arr[4][2], Nat_Flag[4][2], Light[4][2], Nature[4][2])
            out[18] = "11%s  %s  %5.2f   %s\r\n" % (sensi_arr[1][3], Nat_Flag[1][3], Light[1][3], Nature[1][3])
            out[19] = "12%s  %s  %5.2f   %s\r\n" % (sensi_arr[3][3], Nat_Flag[3][3], Light[3][3], Nature[3][3])
            out[20] = "13%s  %s  %5.2f   %s\r\n" % (sensi_arr[5][3], Nat_Flag[5][3], Light[5][3], Nature[5][3])
            out[21] = "14%s  %s  %5.2f   %s\r\n" % (sensi_arr[2][4], Nat_Flag[2][4], Light[2][4], Nature[2][4])

        for i in range(39):
            print_flag = 2
            if print_flag == 0:
                if i >= 6 and i <= 27:
                    continue
            elif print_flag == 1:
                if (i < 6) or (i > 27 and i < 37):
                    continue
            if Base[4] == "检测组合D":
                if i > 21 and i < 28:
                    continue
            print(out[i])
            self.ser.write(out[i].encode("GBK"))


if __name__ == '__main__':
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    #   姓名，性别，样本号，条码号，样本类型，测试时间，打印时间
    Data_Base = ["路人甲", "男", "0123456789", "9876543210", "检测组合D", time_now, time_now]
    Data_Nature = []
    if Data_Base[4] == "检测组合A" or Data_Base[4] == "检测组合B" or Data_Base[4] == "检测组合C":
        Data_Nature = [['弱阳性', '0', '弱阳性', '0', '弱阳性'], ['0', '弱阳性', '0', '阴性', '0'],
                       ['强阳性', '0', '中阳性', '0', '弱阳性'], ['0', '弱阳性', '0', '弱阳性', '0'],
                       ['弱阳性', '0', '弱阳性', '0', '阴性'], ['0', '中阳性', '0', '阴性', '0'],
                       ['阴性', '0', '阴性', '0', '阴性'], ['0', '阴性', '0', '阴性', '0']]
    elif Data_Base[4] == "检测组合D":
        Data_Nature = [['0', '弱阳性', '0', '阴性', '0'], ['弱阳性', '0', '阴性', '0', '弱阳性'],
                       ['0', '弱阳性', '0', '弱阳性', '0'], ['强阳性', '0', '中阳性', '0', '弱阳性'],
                       ['0', '中阳性', '0', '弱阳性', '0'], ['阴性', '0', '阴性', '0', '阴性'],
                       ['0', '阴性', '0', '阴性', '0'], ['阴性', '0', '阴性', '0', '阴性']]
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
