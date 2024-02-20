# coding:utf-8
import subprocess
import os
import time
import sys
import datetime


class Mount_move:
    #   参数设置
    def __init__(self):
        #   文件保存标志，True保存，Flase不保存
        self.Mount_Save = True

        print("_______________________________________________")
        #   创建文件夹目录
        createFloder_path = [
            '../log',
            '../log/log_mount'
        ]
        #   创建文件夹
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                print("%s文件夹已经创建成功！" % i)
            else:
                print("%s文件夹已存在！" % i)

    #   1 复制文件
    def Move(self, original, final, identifier):
        # ----------------------------------------------#
        #   步骤1：执行挂载
        # ----------------------------------------------#
        TAG = "/dev/sda1"
        #   生成挂载文件夹
        if not os.path.exists("/mnt/mydev"):
            #   创建文件夹
            subp = subprocess.Popen(["sudo mkdir /mnt/mydev"],
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
            #   等待
            subp.wait(2)
            #   判断文件创建功能是否执行完毕
            if subp.poll() == 0:  # 执行完成
                print("挂载文件已经创建成功！")
                if subp.stdout.read() != "":
                    print("输出：", subp.stdout.read())
            else:
                print("**挂载文件创建失败！")
                print("**错误：", subp.stderr.read())
        else:
            print("挂载文件已经存在！")
            pass

        #   获取U盘标志
        subp = subprocess.Popen(["sudo fdisk -l"],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        #   等待
        subp.wait(2)
        #   判断功能是否执行完毕
        if subp.poll() == 0:  # 执行完成
            num = -1
            #   循环输出反馈信息
            for index, line in enumerate(subp.stdout.readlines()):
                #   获取到备注的磁盘标识符
                if line == "磁盘标识符：%s\n" % identifier:
                    num = index + 3
                #   根据上述信息，获取U盘标志
                if index == num:
                    TAG = line[0:9]
                    print("成功获取U盘标志！")
        else:
            print("**U盘标志获取失败！")
            print("**错误：", subp.stderr.read())
            pass

        #   执行挂载程序
        stepOne = subprocess.Popen(["sudo mount %s /mnt/mydev" % TAG],
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   encoding='utf-8')
        #   等待
        stepOne.wait(2)
        #   判断功能是否执行完毕
        if stepOne.poll() == 0:  # 执行完成
            print("挂载成功！")
            if stepOne.stdout.read() != "":
                print("输出：", stepOne.stdout.read())
        else:
            print("**挂载失败！")
            print("**错误：", stepOne.stderr.read())
            return False

        # ----------------------------------------------#
        #   步骤2：移动文件
        # ----------------------------------------------#
        file_path = original.split("/")
        file_name = file_path[len(file_path) - 1]
        stepTwo = subprocess.Popen(["sudo cp %s %s" % (original, final)],
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   encoding='utf-8')
        stepTwo.wait(2)
        if stepTwo.poll() == 0:
            print("%s文件复制成功!" % file_name)
            if stepTwo.stdout.read() != "":
                print("输出：", stepTwo.stdout.read())
        else:
            print("**文件复制失败！")
            print("**错误：", stepTwo.stderr.read())

        # ----------------------------------------------#
        #   步骤3：取消挂载
        # ----------------------------------------------#
        stepThree = subprocess.Popen(["sudo umount /mnt/mydev"],
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     encoding='utf-8')
        stepThree.wait(2)
        if stepThree.poll() == 0:
            print("取消挂载成功！")
            if stepThree.stdout.read() != "":
                print("输出：", stepThree.stdout.read())
        else:
            print("**取消挂载失败！")
            print("**错误：", stepThree.stderr.read())

        return True

    #   1 保存输出日志
    def Move_log(self, original, final, identifier):
        #   输出程序执行时间
        start = time.perf_counter()  # 开始时间点
        #   数据暂时存储
        temp = sys.stdout
        #   判断输出到控制台，还是日志中
        if self.Mount_Save == True:
            # 初始化将print输出到文件中
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            # 把输出重定向文件
            print_log = open("./log/log_mount/%s.log" % time_now, 'w')
            # 使用print函数，都将内容打印到日志文件中
            sys.stdout = print_log
        else:
            pass

        #   调用需要保存日志的程序
        flag = self.Move(original, final, identifier)

        end = time.perf_counter()  # 结束时间点
        print("时间消耗：%.2f s" % (end - start))

        #   上述print内容均已输出到文档
        if self.Mount_Save == True:
            sys.stdout = temp
        else:
            pass
        return flag


if __name__ == '__main__':
    mMove = Mount_move()

    ori = "/home/topeet/test/start_rknn.sh"
    fin = "/mnt/mydev"
    id = "0xc009d7d1"

    flag = mMove.Move(ori, fin, id)

    print("操作标志：", flag)
