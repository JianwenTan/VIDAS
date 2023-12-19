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

out = ['0'] * 16


class Em5822_Print:

    def __init__(self):
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            print("无串口设备。")
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值
        # self.ser = serial.Serial("/dev/ttyUSB1", 9600)  # 打开COM17，将波特率配置为115200，其余参数使用默认值

    def em5822_show(self, data):
        print(2)

    def em5822_instruction(self, data):
        print(3)

    def em5822_print(self, time_test, time_now):
        mixture20_A_random = random.randint(0, 19)
        mixture20_A_result = random.randint(0, 3)
        mixture20_B_random = random.randint(0, 19)
        mixture20_B_result = random.randint(0, 3)
        mixture19_random = random.randint(0, 19)
        mixture19_result = random.randint(0, 3)
        synthesis14_random = random.randint(0, 13)
        synthesis14_result = random.randint(0, 3)
        out[0] = "过敏原检验报告单\r\n"
        out[1] = "姓名：XXX    性别：男\r\n"
        out[2] = "样本号：1234567890\r\n"
        out[3] = "条码号：1234567890\r\n"
        out[4] = "样本类型：试剂\r\n"
        out[5] = "测试时间：%s\r\n" % time_test
        out[6] = "--------------------------------"
        out[7] = "过敏原  结果  参考值  结果解释\r\n"
        out[8] = "1" + mixture19[mixture20_A_random] + "  " + result[mixture20_A_result] + \
                 "  -----  " + result_explain[mixture20_A_result]+"\r\n"
        out[9] = "2" + mixture19[mixture20_B_random] + "  " + result[mixture20_B_result] + \
                 "  -----  " + result_explain[mixture20_B_result]+"\r\n"
        out[10] = "3" + mixture19[mixture19_random] + "  " + result[mixture19_result] + \
                  "  -----  " + result_explain[mixture19_result]+"\r\n"
        out[11] = "4" + mixture19[synthesis14_random] + "  " + result[synthesis14_result] + \
                  "  -----  " + result_explain[synthesis14_result]+"\r\n"
        out[12] = "--------------------------------"
        out[13] = "打印时间：%s\r\n" % time_now
        out[14] = "此检疫报告只对此标本负责，请结合临床。\r\n"
        out[15] = "\r\n"

        for i in range(16):
           self.ser.write(out[i].encode("GBK"))


if __name__ == '__main__':
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")

    eprint = Em5822_Print()

    eprint.em5822_print(time_now, time_now)
