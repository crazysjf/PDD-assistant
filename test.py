from datetime import date
import os
from selenium import webdriver

# options = webdriver.ChromeOptions()
# prefs = {"debuggerAddress": "127.0.0.1:9233",
#         'profile.default_content_settings.popups': 0,
#          'download.default_directory': 'C:\\Users\Administrator\\Desktop\\requests_pwrd'}
# options.add_experimental_option('prefs', prefs)
#
# driver = webdriver.Chrome(chrome_options=options)
#


# str = ' 103353683024 '
# print(str.strip())
#

base = r"""D:\projects\20200407-拼多多宝贝搬家助手"""

def get_current_sub_dir(base):
    def construct_path(num):
        return base + "\\" + str(num)

    cont =os.listdir(base)

    try:
        max_num = max(map(int, list(filter(lambda s: s.isdigit(), filter(os.path.isdir, cont)))))
    except:
        max_num = 0

    if max_num == 0 or len(os.listdir(construct_path(max_num))) >= 10:
        max_num = max_num + 1
        os.makedirs(construct_path(max_num))

    return construct_path(max_num)

print(getCurrentSubDir(base))



