from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import cv2
import numpy as np
from io import BytesIO
import time, requests
from lxml import etree
import json
import datetime


class CrackSlider():
    def __init__(self):
        super(CrackSlider, self).__init__()
        self.url = 'http://fin.ane56.com/account/welcome'
        chrome_options = Options()
        chrome_options.add_argument("window-size=1280,1696")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1',options=chrome_options)
        self.wait = WebDriverWait(self.driver, 3)
        self.zoom = 1
        self.i = 0

    def open(self):

        self.driver.get(self.url)

    def get_pic(self):
        time.sleep(2)
        target = self.driver.find_element_by_css_selector('#slide > div > div.validate_main > img.validate_big')
        target.screenshot('target.jpg')
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        print(local_img.size)
        self.zoom = 300 / int(size_loc[0])
    def get_tracks(self, distance):
        print(distance)
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def match(self, target, template,username,password):
        try:
            img_rgb = cv2.imread(target)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(template, 0)
            run = 1
            w, h = template.shape[::-1]
            print(w, h)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            # 使用二分法查找阈值的精确值
            L = 0
            R = 1
            while run < 20:
                run += 1
                threshold = (R + L) / 2
                print(threshold)
                if threshold < 0:
                    print('Error')
                    return None
                loc = np.where(res >= threshold)
                print(len(loc[1]))
                if len(loc[1]) > 1:
                    L += (R - L) / 2
                elif len(loc[1]) == 1:
                    print('目标区域起点x坐标为：%d' % loc[1][0])
                    break
                elif len(loc[1]) < 1:
                    R -= (R - L) / 2
            # print(loc)
            return loc[1][0]
        except:
            self.crack_slider(username,password)

    def crack_slider(self, username, password):
        self.open()
        self.get_pic()
        target = 'target.jpg'
        template = 'qk.png'
        distance = self.match(target, template,username,password)
        tracks = self.get_tracks((distance + 36) * self.zoom)  # 对位移的缩放计算
        try:
            slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'validate_button_icon')))
            ActionChains(self.driver).click_and_hold(slider).perform()

            for track in tracks['forward_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

            time.sleep(0.5)
            for back_tracks in tracks['back_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

            ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.driver).release().perform()
            time.sleep(1.8)


            time.sleep(0.6)

            self.driver.find_element_by_id('username').clear()
            self.driver.find_element_by_id('username').send_keys(username)
            self.driver.find_element_by_id('password').clear()
            self.driver.find_element_by_id('password').send_keys(password)
            time.sleep(0.3)
            self.driver.find_element_by_css_selector(
                '#form > div.login_box_row.login_box_button > input.btn-submit').send_keys(Keys.ENTER)
            time.sleep(0.6)
            content = etree.HTML(self.driver.page_source)
            title = content.xpath('//title/text()')[0]
            # print(title)
            if title == '欢迎页 - 统一结算平台':
                print('系统登录成功')
                mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
                jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
                jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1'
                accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
                aut_url = 'https://fin.ane56.com/account/api/access/auth'
                users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
                cookie = json.dumps(self.driver.get_cookies())
                cookie_dict = json.loads(cookie)
                cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
                cookies = '; '.join(item for item in cookie_list)
                headers = {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Content-Length': '0',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': cookies,
                    'Host': 'fin.ane56.com',
                    'Origin': 'https://fin.ane56.com',
                    'Referer': 'https://fin.ane56.com/account/welcome',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                }
                data = {
                    'siteId': '',
                }
                item = {}
                # 网点基本信息
                site_info = json.loads(requests.post(aut_url, headers=headers).text)
                item['site_name'] = site_info['data']['siteName']
                item['site_id'] = site_info['data']['siteId']
                item['site_type'] = site_info['data']['siteVO']['siteTypeName']
                # 网点用户授权
                user_data = {
                    "code": "",
                    "name": "",
                    "userRole": "",
                    "status": "N",
                    "page": "1",
                    "pageSize": "50",
                    "deptid": item['site_id'],
                }
                getUsers_info = json.loads(requests.post(users_url, data=user_data, headers=headers).text)
                item['getUser'] = getUsers_info
                # 年经营情况
                # print('网点年经营情况:')
                jr_qk = json.loads(requests.post(mjy_url, data=data, headers=headers).text)
                item['BusiDetailByMonth'] = jr_qk['data']

                # 交易费用汇总(昨日)
                # print('交易费用汇总:')
                jy_fyhz = json.loads(requests.post(jyxy_url, headers=headers).text)
                item['yesterdayBusiQuery'] = jy_fyhz['data']
                # 交易费用汇总(本月截止昨日)
                jy_fyhzyj = json.loads(requests.post(jyhzy_url, headers=headers).text)
                item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
                # 网点当前余额
                # print('网点当前余额:')
                accountinfo = json.loads(requests.post(accountinfo_url, headers=headers).text)
                item['AccountInfo'] = accountinfo
                item['code'] = '200'
                item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.close()
                return item

                # return self.caiji()
            else:
                self.i += 1
                if self.i < 3:
                    return self.crack_slider(username, password)
                error_msg = {
                        "msg": "",
                        "code": 600,
                    }
                return error_msg
        except Exception as e:
            error_msg = {
                "msg": "",
                "code": 600,
            }
            return error_msg
    def close(self):
        self.driver.quit()

