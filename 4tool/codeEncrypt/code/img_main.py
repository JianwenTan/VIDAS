# encoding: utf-8
import sys
import datetime

sys.path.append("code_process")
sys.path.append("code_acquire")
sys.path.append("code_print")
sys.path.append("code_mount")

from code_process import imgRun
from code_print import Em5822
from code_mount import mount


class img_main:

    #   初始化
    def __init__(self):
        self.Pro = imgRun.Img_run()
        self.Pri = Em5822.Em5822_out()
        self.Move = mount.Mount_move()

    #   图像处理全流程
    def imgProcess(self, read, write, combina, radius):
        flag, gray, nature = self.Pro.process_log(path_read=read, path_write=write, combina=combina, radius=radius)
        return flag, gray, nature

    #   图像获取初始化
    def imgAcquire_init(self):
        pass

    #   图像获取全流程
    def imgAcquire(self):
        pass

    #   热转印打印初始化
    def natPrint_init(self):
        flag = self.Pri.em5822_init_log()
        return flag

    #   热转印打印
    def natPrint(self, Base, Nature, Data_Light):
        flag = self.Pri.em5822_print_log(Base, Nature, Data_Light)
        return flag

    #   挂载移动文件
    def mountMove(self, original, final, identifier):
        flag = self.Move.Move_log(original, final, identifier)
        return flag

    #   步骤执行
    def Run_step(self, num):
        # -----------------------------------------------------------------------------------#
        #   步骤： 1   图像获取初始化
        #
        #   标志：
        # -----------------------------------------------------------------------------------#
        if num == 1:
            pass
        # -----------------------------------------------------------------------------------#
        #   步骤： 2   初始化热转印打印机
        #   先完成热转印打印初始化；
        #   参数1     Pri_Init_flag   True表示成功初始化，False表示初始化失败
        # -----------------------------------------------------------------------------------#
        elif num == 2:
            print("————————————————————————————————————————————————")
            Pri_Init_flag = Main.natPrint_init()  # 打印初始化
            print("热转印-初始化标志：%s\r\n" % type(Pri_Init_flag), Pri_Init_flag)
            print("————————————————————————————————————————————————")
        # -----------------------------------------------------------------------------------#
        #   步骤： 3   图像获取-全流程
        #
        #   标志：
        # -----------------------------------------------------------------------------------#
        elif num == 3:
            pass
        # -----------------------------------------------------------------------------------#
        #   步骤： 4   图像处理-全流程
        #   一般需先完成图像获取，再执行图像处理
        #   参数1     flag    图像处理成功标志，True-成功，False-失败
        #   参数2     gray    发光矩阵数据，9*5
        #   参数3     nature  过敏原性质矩阵，9*5
        # -----------------------------------------------------------------------------------#
        elif num == 4:
            print("————————————————————————————————————————————————")
            """
            参数1 flag    图像处理成功标志，True-成功，False-失败
            参数2 gray    发光矩阵数据，9*5
            参数3 nature  过敏原性质矩阵，9*5
            """
            flag, gray, nature = Main.imgProcess(read='../img/img_input/2.jpeg', write='../img/img_out/', combina="检测组合A", radius=40)
            print("图像处理-成功标志：%s\r\n" % type(flag), flag)
            print("图像处理-发光矩阵：%s\r\n" % type(gray), gray)
            print("图像处理-性质矩阵：%s\r\n" % type(nature), nature)
            print("————————————————————————————————————————————————")
        # -----------------------------------------------------------------------------------#
        #   步骤： 5   热转印打印数据
        #   **  必须先完成热转印打印初始化，才能进行热转印打印
        #   参数1     Pri_print_flag   True表示成功打印，False表示打印失败
        # -----------------------------------------------------------------------------------#
        elif num == 5:
            print("————————————————————————————————————————————————")
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 打印时间
            time_test = "2024-01-29 17:20:19"  # 测试时间
            #   姓名，性别，样本号，条码号，样本类型，测试时间，打印时间
            Data_Base = ["路人甲", "男", "0123456789", "9876543210", "检测组合A", time_test, time_now]
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
            Pri_print_flag = Main.natPrint(Data_Base, Data_Nature, Data_Light)  # 打印数据
            print("热转印-打印标志：%s\r\n" % type(Pri_print_flag), Pri_print_flag)
            print("————————————————————————————————————————————————")
        # -----------------------------------------------------------------------------------#
        #   步骤： 6   挂载移动文件
        #   **  必须先完成热转印打印初始化，才能进行热转印打印
        #   参数1     Mount_flag   True表示成功挂载移动，False表示挂载移动失败
        # -----------------------------------------------------------------------------------#
        elif num == 6:
            print("————————————————————————————————————————————————")
            original = "/home/topeet/test/start_rknn.sh"  # 表示需要移动文件
            final = "/mnt/mydev"  # 表示U盘挂载位置
            identifier = "0xc009d7d1"  # 表示U盘标识符
            Mount_flag = Main.mountMove(original, final, identifier)  # 打印初始化
            print("挂载移动标志：%s\r\n" % type(Mount_flag), Mount_flag)
            print("————————————————————————————————————————————————")
        else:
            pass


if __name__ == '__main__':
    Main = img_main()

    Main.Run_step(4)
    # Main.Run_step(5)
