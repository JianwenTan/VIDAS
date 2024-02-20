import subprocess
import os
import time
import sys
import datetime


class Mount_move:
    def __init__(self):
        self.Mount_Save = True

        pass
        createFloder_path = [
            '../log',
            '../log/log_mount'
        ]
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                pass
            else:
                pass

    def Move(self, original, final, identifier):
        TAG = "/dev/sda1"
        if not os.path.exists("/mnt/mydev"):
            subp = subprocess.Popen(["sudo mkdir /mnt/mydev"],
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
            subp.wait(2)
            if subp.poll() == 0:  
                pass
                if subp.stdout.read() != "":
                    pass
            else:
                pass
                pass
        else:
            pass
            pass

        subp = subprocess.Popen(["sudo fdisk -l"],
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
        subp.wait(2)
        if subp.poll() == 0:  
            num = -1
            for index, line in enumerate(subp.stdout.readlines()):
                if line == "磁盘标识符：%s\n" % identifier:
                    num = index + 3
                if index == num:
                    TAG = line[0:9]
                    pass
        else:
            pass
            pass
            pass

        stepOne = subprocess.Popen(["sudo mount %s /mnt/mydev" % TAG],
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   encoding='utf-8')
        stepOne.wait(2)
        if stepOne.poll() == 0:  
            pass
            if stepOne.stdout.read() != "":
                pass
        else:
            pass
            pass
            return False

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
            pass
            if stepTwo.stdout.read() != "":
                pass
        else:
            pass
            pass

        stepThree = subprocess.Popen(["sudo umount /mnt/mydev"],
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     encoding='utf-8')
        stepThree.wait(2)
        if stepThree.poll() == 0:
            pass
            if stepThree.stdout.read() != "":
                pass
        else:
            pass
            pass

        return True

    def Move_log(self, original, final, identifier):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Mount_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./log/log_mount/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.Move(original, final, identifier)

        end = time.perf_counter()  
        pass

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

    pass
