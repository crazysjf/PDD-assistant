
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
import utils as utils
import time, sys
import os
from datetime import date
import urllib.request


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class WebOperator(Singleton):
    def __init__(self):




        chrome_options =  webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9233")
        # chrome_options.add_experimental_option("profile.default_content_settings.popups", 0)
        # chrome_options.add_experimental_option("download.default_directory", save_dir)




        # 设置下载地址、禁止弹窗
        # prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': save_dir}
        # chrome_options.add_experimental_option('prefs', prefs)
        self._driver = webdriver.Chrome(chrome_options=chrome_options)

        # 默认等待时间10秒
        self._driver.implicitly_wait(10)

    def fill_properties_for_good(self):
        

    def get_good_id_list(self):
        self._driver.implicitly_wait(0)
        ret = []
        # 商品素材
        #self._driver.get("https://mms.pinduoduo.com/goods/goods_materials")
        #input("确保每页宝贝数是最大（100），并且加载完毕。按任意键继续...")

        # es = self._driver.find_elements_by_css_selector("div.goodsInfo div.goods-id")
        # for e in es:
        #     print(e.text)
        #trs = self._driver.find_elements_by_css_selector("div.materialsTableList table tbody tr")
        trs = self._driver.find_elements_by_xpath("//div[@class='materialsTableList']//div[@class='TB_innerMiddle_290']//table//tbody//tr")
        #print(len(trs))
        i = 0
        for tr in trs:
            #i = i+1
            #print(i, tr.text)
            # 判断是否已经存在白底图
            has_wbg_pic = False
            image_statuses = tr.find_elements_by_xpath(".//div[@class='materialsPicContainer']//div[@class='imageStatus']")
            #print(image_statuses)
            if len(image_statuses) != 0:
                if image_statuses[0].text != "":
                    has_wbg_pic = True

            ids = tr.find_elements_by_xpath(".//div[@class='goods-id']")
            if len(ids) != 0:
                id_text = ids[0].text # "ID : 103353683024
                id = id_text.split(":")[1].strip()
                if has_wbg_pic == False:
                    if id  not in ret: # 防止xpath的bug导致ID重复，trs会有重复记录
                        ret.append(id)


        self._driver.implicitly_wait(10)
        #print(ret)
        return ret

    # 1个文件夹只能放10个文件，不够时创建新文件夹
    def get_current_sub_dir(self, base):
        def construct_path(num):
            return base + "\\" + str(num)

        cont = os.listdir(base)

        try:
            max_num = max(map(int, list(filter(lambda s: s.isdigit(), filter(lambda p:os.path.isdir(os.path.join(base, p)), cont)))))
        except:
            max_num = 0

        if max_num == 0 or len(os.listdir(construct_path(max_num))) >= 10:
            max_num = max_num + 1
            d = construct_path(max_num)
            if not os.path.exists(d):
                os.makedirs(d)
                return d

        return construct_path(max_num)

    def download_wbg_pic(self, id):
        save_dir = os.path.dirname(os.path.abspath(__file__)) + "\\白底-" + str(date.today())
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 每次只能上传10张白底，把白底放到多个文件夹中，每个文件夹10张图
        num_dir = self.get_current_sub_dir(save_dir)

        base_url = "https://mms.pinduoduo.com/goods/goods_detail?goods_id="
        url = base_url + id
        self._driver.get(url)

        pics = self._driver.find_elements_by_css_selector("div.item-list-text div.image-list img")
        # for pic in pics:
        #     url = pic.get_attribute("src")
        #     print(url)

        # 第五张固定为白底
        pic_url = pics[4].get_attribute("src")

        urllib.request.urlretrieve(pic_url, num_dir + "\\" + id + "-wbg.jpg")
        print("downloaded: " + id)

    def meizhe_set_clearance_price_for_one_good(self, code):
        """
        
        :param code: 
        :return: 返回（原价, 清仓价)，如果没有找到任何商品，返回None 
        """
        # 注意选择子的使用，必须保证在两个界面（第一次搜索和之后）都能使用
        search_box_ele = self._driver.find_element_by_css_selector("input.mz-form-control.mz-input")

        search_box_ele.clear()
        search_box_ele.send_keys(code + Keys.RETURN)
        # main-content > div:nth-child(2) > div.mz-nav-block > ul > li.pull-right > form > input


        # 这里需要判断有没有查找到相应的商品。
        # 需要通过 div.mz-edit-all-items div.mz-alert 的style属性判断
        # 该div用于显示“没有找到任何打折商品”的提示。
        # 无论有没有找到商品，该div都会存在，只是找到商品的情况下style会被设为display:none

        # 页面使用ajax加载，警告框似乎一直存在，此处只能等待
        time.sleep(1)
        allert_div = self._driver.find_element_by_css_selector("div.mz-edit-all-items div.mz-alert")

        # 有警告框（style="display: none 不存在），就不用继续了
        if "none" not in allert_div.get_attribute("style"):
            return None

        price_input = self._driver.find_element_by_css_selector("div.final-price input")

        # 获取原价
        orig_price = float(price_input.get_attribute("value"))

        price_input.clear()

        clearance_price = utils.calc_clearance_price(orig_price)
        price_input.send_keys(str(clearance_price))
        while(True):
            try:
                summit_button = self._driver.find_element_by_css_selector("div.fast-submit a.btn-primary")
                summit_button.click()
                break
            except:
                print("Unexpected error wile clicking:", sys.exc_info()[0])
                time.sleep(1)


        return (orig_price, clearance_price)

    def cjdz_start_operation(self):
        # 进入批量修改类目界面
        self._driver.get("https://qnxg.superboss.cc/index.html#/index/index/?type=6")

        # 切换到“勾选商品”tab，等3秒
        tab = self._driver.find_element_by_css_selector('div[data-type="commodity"]')
        tab.click()
        time.sleep(3)

    def cjdz_check_one_good(self, code):
        """
        勾选一个商品
        :param code: 
        :return: 成功勾选返回True，找不到返回False
        """
        search_box_ele = self._driver.find_element_by_css_selector('div.search input[name="searchbar"')

        search_box_ele.clear()
        search_box_ele.send_keys(code + Keys.RETURN)

        # 页面使用ajax加载，警告框似乎一直存在，此处只能等待
        time.sleep(1)

        # 判断是不是找不到任何宝贝
        status_div = None
        # 暂时取消隐式超时，因为需要立马返回查找元素的结果
        self._driver.implicitly_wait(0)

        try:
            status_div = self._driver.find_element_by_css_selector("div.listContent div.next-status-content")
        except:
            pass

        self._driver.implicitly_wait(10)

        # status_div如果存在表明没有找到任何宝贝
        if status_div != None:
            return False
        while (True):
            try:
                checkbox = self._driver.find_element_by_css_selector("div.listContent i.next-icon")
                checkbox.click()
                break
            except:
                print("Unexpected error wile clicking:", sys.exc_info()[0])
                time.sleep(1)

        return True