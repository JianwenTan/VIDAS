# coding:utf-8
#   打包程序
import shutil

from setuptools import setup
from Cython.Build import cythonize
import os

# runFlag = "N"
runFlag = input("是否执行删除程序：")
# ----------------------------------------------#
#   步骤1：程序打包
# ----------------------------------------------#
#   程序打包目录
dir_paths = ['./code/code_acquire',
             './code/code_mount',
             './code/code_em5822',
             './code/code_process'
             ]

#   程序打包文件遍历
files = [i + '/*.py' for i in dir_paths]

#   程序打包过程
setup(ext_modules=cythonize(files))

# ----------------------------------------------#
#   步骤2：移动源文件,并删除没必要的文件
# ----------------------------------------------#
#   程序删除目录
del_paths = ['./build',
             './dist',
             './UNKNOWN.egg-info',
             './code/code_mount/refer'
             ]
#   移动文件，并删除文件
if os.path.exists("./build"):
    #   获取打包目录的后缀,win-amd64-cpython-38
    dir_suffix = ""
    for i in os.listdir("./build"):
        if i.split('.', 1)[0] == "lib":
            dir_suffix = i.split('.', 1)[1]
    #   获取打包源码的后缀,cp38-win_amd64.pyd
    file_suffix = os.listdir("./build/lib.%s" % dir_suffix)[0].split('.', 1)[1]
    #   遍历code目录下的文件
    for i in dir_paths:
        #   目录下的py源文件
        source_files = []
        #   扫描目录下的所有文件
        files = os.listdir("%s" % i)
        #   遍历目前中的所有文件
        for j in files:
            if ".py" in j:  # 判断目前中py文件
                files_name = j.split('.')[0]
                source_files.append(files_name)
        #   移动打包文件，并删除原始文件
        for k in source_files:
            if os.path.exists("%s/%s.%s" % (i, k, file_suffix)):
                os.remove("%s/%s.%s" % (i, k, file_suffix))
            else:
                shutil.move("./build/lib.%s/%s.%s" % (dir_suffix, k, file_suffix), i)
            #   删除c文件
            if os.path.exists("%s/%s.c" % (i, k)):
                os.remove("%s/%s.c" % (i, k))
            if runFlag == "y":
                #   删除py文件
                if os.path.exists("%s/%s.py" % (i, k)):
                    os.remove("%s/%s.py" % (i, k))
    #   删除其余文件
    for m in del_paths:
        if os.path.exists("%s" % m):
            shutil.rmtree("%s" % m)
            print("%s文件已经删除！" % m)
        else:
            print("%s文件不存在！" % m)
else:
    print("build文件夹不存在！")

# ----------------------------------------------#
#   步骤3：生成所需文件夹
# ----------------------------------------------#
#   创建文件夹目录
createFloder_path = [
    './img',
    './img/img_cache',
    './img/img_input',
    './img/img_out',
    './log',
    './log/log_mount',
    './log/log_printInit',
    './log/log_printRun',
    './log/log_process',
    './log/log_acquireInit',
    './log/log_acquireRun'
]
if runFlag == "y":
    #   创建文件夹
    for i in createFloder_path:
        if not os.path.exists("%s" % i):
            os.makedirs("%s" % i)
            print("%s文件夹已经创建成功！" % i)
        else:
            print("%s文件夹已存在！" % i)
else:
    print("还未删除源程序！")
