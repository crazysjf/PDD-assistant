# 属性填写器


import utils as utils
import sys
from openpyxl import load_workbook
import openpyxl.styles as sty
import web_operator as web_operator



wo = web_operator.WebOperator()
id_list = wo.get_good_id_list()

print("无白底图ID(总数：%d)：" % len(id_list), id_list)
input("按任意键继续...")

for id in id_list:
    wo.download_wbg_pic(id)