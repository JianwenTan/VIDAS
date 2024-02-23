# encoding: utf-8
import re
import os

#   程序去掉注释目录
dir_paths = ['./Code/code_acquire',
             './Code/code_mount',
             './Code/code_em5822',
             './Code/code_process'
             ]


# ----------------------------------------------#
#   去掉注释
# ----------------------------------------------#
def remove_comments(code):
    #   去掉单行注释，并去掉当前空行
    code = re.sub(r'(?m)^[\t ]*#.*\n?', '', code)
    #   去掉代码后面的注释
    code = re.sub(r'#.*', '', code)
    #   去掉多行注释
    code = re.sub(r'(?s)""".*"""', '', code)
    #   去掉多行注释
    code = re.sub(r"(?s)'''.*?'''", '', code)
    #   去掉所有print函数
    code = re.sub(r'print(.*)', 'pass', code)
    return code


# ----------------------------------------------#
#   遍历文件
# ----------------------------------------------#
#   判断是否存在code文件夹
if os.path.exists("./code"):
    for i in dir_paths:  # 去掉注释的目录
        files = os.listdir("%s" % i)  # 遍历目录中的所有文件
        for j in files:  # 去掉注释的文件
            if ".py" in j:  # 判断目录中的py文件
                #   读取文件
                with open('%s/%s' % (i, j), encoding='utf-8') as file:
                    code = file.read()
                #   去掉注释
                new_code = remove_comments(code)
                #   保存文件
                with open('%s/%s' % (i, j), 'w+', encoding='utf-8') as new_file:
                    new_file.write(new_code)
else:
    print("code文件夹不存在！")
