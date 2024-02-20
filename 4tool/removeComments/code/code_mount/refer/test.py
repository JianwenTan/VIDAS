import subprocess

subp = subprocess.Popen(["sudo fdisk -l"],
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8')

subp.wait(2)
pass
if subp.poll() == 0:
    pass
    num_loca = -1
    for index, line in enumerate(subp.stdout.readlines()):
        if line == "磁盘标识符：0xc009d7d1\n":
            num_loca = index + 3
            pass
        if index == num_loca:
            pass
    pass
else:
    pass
    pass
    pass
