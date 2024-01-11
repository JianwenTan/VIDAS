import random
import datetime

import serial
import serial.tools.list_ports

mixture20_A = [
    '螨混合  ', '蟑螂    ', '霉菌混合', '悬铃木  ', '榆树    ',
    '葎草    ', '艾蒿    ', '普通豚草', '猫上皮  ', '狗上皮  ',
    '小麦    ', '花生    ', '鸡蛋    ', '大豆    ', '牛奶    ',
    '西红柿  ', '鳕鱼    ', '虾      ', '蟹     ', '开心果  '
]

mixture20_B = [
    '牛奶    ', '花生    ', '蛋清    ', '大豆    ', '艾蒿    ',
    '屋尘螨  ', '交链孢霉', '普通豚草', '狗上皮  ', '猫上皮  ',
    '蜜蜂毒  ', '棉絮    ', '蚊子唾液', '烟草屑  ', '霉菌混合',
    '苦艾    ', '蒲公英  ', '柏树    ', '草花粉  ', '树木花粉'
]

mixture19 = [
    '柳树    ', '普通豚草', '艾蒿    ', '屋尘螨  ', '屋尘    ',
    '猫上皮  ', '狗上皮  ', '蟑螂    ', '点青霉  ', '葎草    ',
    '蛋清    ', '牛奶    ', '花生    ', '大豆    ', '牛肉    ',
    '羊肉    ', '鳕鱼    ', '虾      ', '蟹      ', 'CCD     '
]

synthesis14 = [
    '屋尘螨  ', '屋尘    ', '柏树    ', '普通豚草', '点青霉  ',
    '猫上皮  ', '狗上皮  ', '蛋清    ', '牛奶    ', '鳕鱼    ',
    '虾      ', '牛肉    ', '芒果    ', '花生    '
]

result = [
    '-', '+', '++', '+++'
]

result_explain = [
    '  阴性', '  弱阳', '  中阳', '  强阳'
]

out = ['0'] * 22


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

    def em5822_print(self, Base, ):
        mixture20_A_random = random.randint(0, 19)
        mixture20_A_result = random.randint(0, 3)
        mixture20_B_random = random.randint(0, 19)
        mixture20_B_result = random.randint(0, 3)
        mixture19_random = random.randint(0, 19)
        mixture19_result = random.randint(0, 3)
        synthesis14_random = random.randint(0, 13)
        synthesis14_result = random.randint(0, 3)
        out[0] = "        过敏原检验报告单\r\n"  # 8个空
        out[1] = "姓名：%s      性别:%s\r\n" % (Base[0], Base[1])
        out[2] = "样本号：%s\r\n" % Base[2]
        out[3] = "条码号：%s\r\n" % Base[3]
        out[4] = "样本类型：%s\r\n" % Base[4]
        out[5] = "测试时间：%s\r\n" % Base[5]
        out[6] = "--------------------------------"
        out[7] = "过敏原  结果  参考值  结果解释\r\n"
        out[8] = "1" + mixture19[mixture20_A_random] + "  " + result[mixture20_A_result] + \
                 "  -----  " + result_explain[mixture20_A_result] + "\r\n"
        out[9] = "2" + mixture19[mixture20_B_random] + "  " + result[mixture20_B_result] + \
                 "  -----  " + result_explain[mixture20_B_result] + "\r\n"
        out[10] = "3" + mixture19[mixture19_random] + "  " + result[mixture19_result] + \
                  "  -----  " + result_explain[mixture19_result] + "\r\n"
        out[11] = "4" + mixture19[synthesis14_random] + "  " + result[synthesis14_result] + \
                  "  -----  " + result_explain[synthesis14_result] + "\r\n"
        out[12] = "————————————————"
        out[13] = "注：\r\n"
        out[14] = "'-'为阴性，<0.35IU/mL\r\n"
        out[15] = "'+'为弱阳性，0.35IU/mL-3.5IU/mL\r\n"
        out[16] = "'++'为中阳性，3.5IU/mL-17.5IU/mL\r\n"
        out[17] = "'+++'为强阳性，≥17.5IU/mL\r\n"
        out[18] = "--------------------------------"
        out[19] = "打印时间：%s\r\n" % Base[6]
        out[20] = "    此检疫报告只对此标本负责，请结合临床。\r\n"
        out[21] = "\r\n"

        # for i in range(22):
        #     self.ser.write(out[i].encode("GBK"))


if __name__ == '__main__':
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    #   姓名，性别，样本号，条码号，样本类型，测试时间，打印时间
    Data_Base = ["路人甲", "男", "0123456789", "9876543210", "检测组合A", time_now, time_now]
    Data_Nature = [['弱阳性', '0', '弱阳性', '0', '弱阳性'], ['0', '弱阳性', '0', '阴性', '0'],
                   ['强阳性', '0', '中阳性', '0', '弱阳性'], ['0', '弱阳性', '0', '弱阳性', '0'],
                   ['弱阳性', '0', '弱阳性', '0', '阴性'], ['0', '中阳性', '0', '阴性', '0'],
                   ['阴性', '0', '阴性', '0', '阴性'], ['0', '阴性', '0', '阴性', '0']]
    print(Data_Nature)
    eprint = Em5822_Print()

    eprint.em5822_print(Data_Base)
