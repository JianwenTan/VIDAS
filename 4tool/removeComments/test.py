# encoding: utf-8
import re
import os

with open('./code/img_main.py', encoding='utf-8') as file:
    code = file.read()

new_code = re.sub(r'print(.*)', 'pass', code)
#   去掉注释
# new_code = remove_comments(code)
#   保存文件
with open('./code/img_main1.py', 'w+', encoding='utf-8') as new_file:
    new_file.write(new_code)