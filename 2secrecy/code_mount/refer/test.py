# coding:utf-8
import subprocess

subp = subprocess.Popen(["sudo fdisk -l"],
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8')

subp.wait(2)
print(subp.poll())
# print(subp.returncode)
if subp.poll() == 0:
    print('1')
    num_loca = -1
    for index, line in enumerate(subp.stdout.readlines()):
        # print(line)
        if line == "磁盘标识符：0xc009d7d1\n":
            num_loca = index + 3
            print(index)
        if index == num_loca:
            print(line[0:9])
    print(subp.stderr.read())
else:
    print('2')
    print(subp.stdout.read())
    print(subp.stderr.read())
