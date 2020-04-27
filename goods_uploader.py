def usage():
    print('''
py <file_name> <working_dir>
生成需要从淘宝上传至拼多多中的宝贝列表。

working_dir里面必须有3个文件：
拼多多商品列表.xlsx -- 拼多多的超级店长导出
淘宝商品列表.xlsx -- 淘宝的超级店长导出

''')

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import sys
from datetime import datetime, date, timedelta
import getopt
import os, re

try:
    options, args = getopt.getopt(sys.argv[1:], "h", ["help"])
except getopt.GetoptError:
    usage()
    sys.exit()

if len(args) != 1:
    print("Error: 必须有1个参数用于指定文件夹名称")
    usage()
    exit(-1)

dir = args[0]
fs = os.listdir(dir)

for f in fs:
    m = re.match('^[^~].*全店SPU导出.*\.xls$', f)
    if m != None:
        pdd_file = dir + "/" + f


    m = re.match('^[^~].*itemList\.xlsx$', f)
    if m != None:
        tb_file = dir + "/" + f

#print(pdd_file, tb_file)

df_pdd =  pd.read_excel(pdd_file)
df_tb = pd.read_excel(tb_file)

# 非清仓款的索引
idx_n_clearance = df_tb['宝贝标题'].apply(lambda r: not r.startswith("清仓"))
#print(idx_n_clearance)


# 拼多多不存在商品索引
pdd_codes = df_pdd["商品编码"]

idx_n_exist = ~df_tb["商家编码"].isin(pdd_codes)
#print(idx_n_exist)


idx = idx_n_clearance & idx_n_exist
ids = df_tb[idx]["宝贝ID"]

# for id in ids:
#     print("https://item.taobao.com/item.htm?id=%s" % id)
print(ids.tolist())
df = pd.DataFrame({"链接":list(map(lambda id:"https://item.taobao.com/item.htm?id=%s" % id, ids))})

df.to_excel(os.path.join(dir, "结果.xlsx"))

