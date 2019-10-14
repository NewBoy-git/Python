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
import threading
import calendar

an_headers = {}


class CrackSlider():
    def __init__(self):
        super(CrackSlider, self).__init__()
        self.url = 'http://fin.ane56.com/account/welcome'
        chrome_options = Options()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 0.3)
        self.zoom = 1
        # self.i = 0

    def open(self):
        self.driver.get(self.url)

    def get_pic(self):
        time.sleep(0.6)
        target = self.driver.find_element_by_css_selector('#slide > div > div.validate_main > img.validate_big')
        target.screenshot('target.jpg')
        pic = cv2.imread('target.jpg')
        pic = cv2.resize(pic, (600, 326), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('target.jpg', pic)
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
            # s = v * t + 0.5 * a * (t ** 2)
            s = v * t
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def match(self, target, template, username, password):
        # try:
        # template = 'qk3.png'
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
        print(loc)
        return loc[1][0]

    # except Exception as e:
    # print(e)
    # return self.crack_slider(username,password)
    def crack_slider(self, username, password):
        sta = datetime.datetime.now()
        self.open()
        end_wb = datetime.datetime.now()
        print('网页访问时间' + str(end_wb - sta))
        target = 'target.jpg'
        template = '/home/xihonglin/Flask/SiteCrawlApi1.0/Spiders/qk3.png'
        self.get_pic()
        distance = self.match(target, template, username, password)
        tracks = self.get_tracks((distance + 7) * self.zoom)  # 对位移的缩放计算
        end = datetime.datetime.now()
        print('验证码图片对比处理耗时:' + str(end - sta))
        try:
            slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'validate_button_icon')))
            ActionChains(self.driver).click_and_hold(slider).perform()

            for track in tracks['forward_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

            # time.sleep(0.5)
            for back_tracks in tracks['back_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

            ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
            # time.sleep(0.5)
            ActionChains(self.driver).release().perform()
            # time.sleep(1.8)
            # time.sleep(0.6)
            end = datetime.datetime.now()
            print('验证码处理总耗时:' + str(end - sta))
            self.driver.find_element_by_id('username').clear()
            self.driver.find_element_by_id('username').send_keys(username)
            self.driver.find_element_by_id('password').clear()
            self.driver.find_element_by_id('password').send_keys(password)
            time.sleep(0.3)
            self.driver.find_element_by_css_selector(
                '#form > div.login_box_row.login_box_button > input.btn-submit').click()
            time.sleep(0.6)
            content = etree.HTML(self.driver.page_source)
            title = content.xpath('//title/text()')[0]
            if title == '欢迎页 - 统一结算平台':
                time.sleep(0.6)
                cookie = json.dumps(self.driver.get_cookies())
                cookie_dict = json.loads(cookie)
                cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
                cookies = '; '.join(item for item in cookie_list)
                print('系统登录成功')
                end1 = datetime.datetime.now()
                print('系统登录耗时:' + str(end1 - sta))
                print(cookie_list)
                print(cookies)
                # mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
                # jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
                # jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1'
                # accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
                # code_url = 'http://api2.sz789.net:88/RecvByte.ashx'
                # aut_url = 'https://fin.ane56.com/account/api/access/auth'
                # users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
                # fhf_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiDetailSummaryVo'
                # finlist_url = 'https://fin.ane56.com/account/api/financeAccountMgr/queryFinAccountList'
                # cookie = json.dumps(self.driver.get_cookies())
                # cookie_dict = json.loads(cookie)
                # cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
                # cookies = '; '.join(item for item in cookie_list)
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
                an_headers['headers'] = headers
                an_headers['code'] = 0
                self.close()
                return an_headers
            else:
                an_headers['headers'] = ''
                an_headers['code'] = 1
                self.close()
                return an_headers
        except Exception as e:
            print(e)
            an_headers['headers'] = ''
            an_headers['headers'] = 0
            self.close()
            return an_headers

    def close(self):
        self.driver.quit()


mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1'
accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
code_url = 'http://api2.sz789.net:88/RecvByte.ashx'
aut_url = 'https://fin.ane56.com/account/api/access/auth'
users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
fhf_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiDetailSummaryVo'
finlist_url = 'https://fin.ane56.com/account/api/financeAccountMgr/queryFinAccountList'
item = {}
gLock = threading.Lock()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
monthRange = calendar.monthrange(year, month - 1)
monthRange = monthRange[1]


# 用户权限列表
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=an_headers['headers']).text)
        gLock.acquire()
        item['site_name'] = site_info['data']['siteName']
        item['site_id'] = site_info['data']['siteId']
        item['site_type'] = site_info['data']['siteVO']['siteTypeName']
        gLock.release()
        user_data = {
            "code": "",
            "name": "",
            "userRole": "",
            "status": "N",
            "page": "1",
            "pageSize": "50",
            "deptid": item['site_id'],
        }
        getUsers_info = json.loads(requests.post(users_url, data=user_data, headers=an_headers['headers']).text)
        gLock.acquire()
        item['getUser'] = getUsers_info
        gLock.release()


# 年经营情况
class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        data = {
            'siteId': '',
        }
        jr_qk = json.loads(requests.post(mjy_url, data=data, headers=an_headers['headers']).text)
        gLock.acquire()
        item['BusiDetailByMonth'] = jr_qk['data']
        gLock.release()


# 交易费用汇总(昨日)
class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        jy_fyhz = json.loads(requests.post(jyxy_url, headers=an_headers['headers']).text)
        gLock.acquire()
        item['yesterdayBusiQuery'] = jy_fyhz['data']
        gLock.release()


# 交易费用汇总(本月截止昨日)
class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        jy_fyhzyj = json.loads(requests.post(jyhzy_url, headers=an_headers['headers']).text)
        gLock.acquire()
        item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
        gLock.release()


# 网点当前余额
class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        accountinfo = json.loads(requests.post(accountinfo_url, headers=an_headers['headers']).text)
        gLock.acquire()
        item['AccountInfo'] = accountinfo
        item['code'] = '200'
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gLock.release()


# 网点近一年发货费
class G(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=an_headers['headers']).text)
        data_send = {
            'page': '1',
            'pageSize': '50',
            'bol': '0',
            'loginSiteId': '',
            'isEwbNo': 'false',
            'orderNos': '',
            'radioDate': '0',
            'isFill': 'false',
            'isFillNo': 'false',
            'startTime': '{}/{}/1 00:00:00'.format(year - 1, month),
            'endTime': '{}/{}/{} 23:59:59'.format(year, month - 1, monthRange),
            'accountId': '',
            'depositSiteId': '1617',
            'depositSiteName': '直营财务中心',
            'siteId': site_info['data']['siteId'],
            'siteName': site_info['data']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': site_info['data']['siteId'],
            'sendSiteName': site_info['data']['siteName'],
            'signSiteId': '',
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteName'],
            'firstSite[siteId]': site_info['data']['siteId'],
            'ewbNoType': '',
            'parentChargeItemId': '176',
        }
        gLock.acquire()
        item['sendBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=data_send, headers=an_headers['headers']).text)
        gLock.release()


class H(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=an_headers['headers']).text)
        senddata_fine = {
            'page': '1',
            'pageSize': '50',
            'bol': '0',
            'loginSiteId': '',
            'isEwbNo': 'false',
            'orderNos': '',
            'radioDate': '0',
            'isFill': 'false',
            'isFillNo': 'false',
            'startTime': '{}/{}/1 00:00:00'.format(year - 1, month),
            'endTime': '{}/{}/{} 23:59:59'.format(year, month - 1, monthRange),
            'accountId': '',
            'depositSiteId': '1617',
            'depositSiteName': '直营财务中心',
            'siteId': site_info['data']['siteId'],
            'siteName': site_info['data']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '101',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': site_info['data']['siteId'],
            'sendSiteName': site_info['data']['siteName'],
            'signSiteId': '',
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteName'],
            'firstSite[siteId]': site_info['data']['siteId'],
            'ewbNoType': '',
            'singSiteName': '',
        }
        gLock.acquire()
        item['sendfineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=senddata_fine, headers=an_headers['headers']).text)
        gLock.release()


class I(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=an_headers['headers']).text)
        receivedata_fine = {
            'page': '1',
            'pageSize': '50',
            'bol': '0',
            'loginSiteId': '',
            'isEwbNo': 'false',
            'orderNos': '',
            'radioDate': '30',
            'isFill': 'false',
            'isFillNo': 'false',
            'startTime': '{}/{}/1 00:00:00'.format(year - 1, month),
            'endTime': '{}/{}/{} 23:59:59'.format(year, month - 1, monthRange),
            'accountId': '',
            'depositSiteId': '1617',
            'depositSiteName': '直营财务中心',
            'siteId': site_info['data']['siteId'],
            'siteName': site_info['data']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '101',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': '',
            'sendSiteName': '',
            'signSiteId': site_info['data']['siteId'],
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteName'],
            'firstSite[siteId]': site_info['data']['siteId'],
            'ewbNoType': '',
            'singSiteName': site_info['data']['siteName'],
        }
        gLock.acquire()
        item['receivefineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=receivedata_fine, headers=an_headers['headers']).text)
        gLock.release()


class J(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=an_headers['headers']).text)
        allfine_data = {
            'page': '1',
            'pageSize': '50',
            'bol': '0',
            'loginSiteId': '',
            'isEwbNo': 'false',
            'orderNos': '',
            'radioDate': '0',
            'isFill': 'false',
            'isFillNo': 'false',
            'startTime': '{}/{}/1 00:00:00'.format(year - 1, month),
            'endTime': '{}/{}/{} 23:59:59'.format(year, month - 1, monthRange),
            'accountId': '',
            'depositSiteId': '1617',
            'depositSiteName': '直营财务中心',
            'siteId': site_info['data']['siteId'],
            'siteName': site_info['data']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '101',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': '',
            'sendSiteName': '',
            'signSiteId': '',
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteName'],
            'firstSite[siteId]': site_info['data']['siteId'],
            'ewbNoType': '',
            'singSiteName': '',
        }
        gLock.acquire()
        item['allfineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=allfine_data, headers=an_headers['headers']).text)
        gLock.release()


def an_spider(username, password):
    c = CrackSlider()
    headers_data = c.crack_slider(username, password)
    if headers_data['code'] == 0:
        t1 = B()
        t1.start()
        t2 = C()
        t2.start()
        t3 = D()
        t3.start()
        t4 = E()
        t4.start()
        t5 = F()
        t5.start()
        t6 = G()
        t6.start()
        t7 = H()
        t7.start()
        t8 = I()
        t8.start()
        t9 = J()
        t9.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        return item
    else:
        err_msg = {
            "msg": "",
            "code": 600,
        }
        return err_msg
#                 year = datetime.datetime.now().year
#                 month = datetime.datetime.now().month
#                 data = {
#                     'siteId': '',
#                 }
#                 item = {}
#                 # 网点基本信息
#                 site_info = json.loads(requests.post(aut_url, headers=headers).text)
#                 item['site_name'] = site_info['data']['siteName']
#                 item['site_id'] = site_info['data']['siteId']
#                 item['site_type'] = site_info['data']['siteVO']['siteTypeName']
#                 # 网点用户授权
#                 user_data = {
#                     "code": "",
#                     "name": "",
#                     "userRole": "",
#                     "status": "N",
#                     "page": "1",
#                     "pageSize": "50",
#                     "deptid": item['site_id'],
#                 }
#                 getUsers_info = json.loads(requests.post(users_url, data=user_data, headers=headers).text)
#                 item['getUser'] = getUsers_info
#                 # 年经营情况
#                 # print('网点年经营情况:')
#                 jr_qk = json.loads(requests.post(mjy_url, data=data, headers=headers).text)
#                 item['BusiDetailByMonth'] = jr_qk['data']
#
#                 # 交易费用汇总(昨日)
#                 # print('交易费用汇总:')
#                 jy_fyhz = json.loads(requests.post(jyxy_url, headers=headers).text)
#                 item['yesterdayBusiQuery'] = jy_fyhz['data']
#                 # 交易费用汇总(本月截止昨日)
#                 jy_fyhzyj = json.loads(requests.post(jyhzy_url, headers=headers).text)
#                 item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
#                 # 网点当前余额
#                 # print('网点当前余额:')
#                 accountinfo = json.loads(requests.post(accountinfo_url, headers=headers).text)
#                 item['AccountInfo'] = accountinfo
#                 #网点近一年发货费
#                 import calendar
#                 monthRange = calendar.monthrange(year,month-1)
#                 monthRange = monthRange[1]
#                 print(monthRange)
#                 data_send = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime':'{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': site_info['data']['siteName'],
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType':'',
#                 'parentChargeItemId':'176',
#                 }
#                 item['sendBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=data_send,headers=headers).text)
#                 data_receive={
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': '',
#                 'signSiteId': site_info['data']['siteId'],
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': site_info['data']['siteName'],
#                 }
#                 #item['receiveBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=data_receive,headers=headers).text)
#                 senddata_fine = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime':'{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': site_info['data']['siteName'],
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': '',
#                 }
#                 item['sendfineBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=senddata_fine,headers=headers).text)
#                 receivedata_fine = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '30',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': '',
#                 'sendSiteName': '',
#                 'signSiteId': site_info['data']['siteId'],
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': site_info['data']['siteName'],
#                 }
#                 item['receivefineBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=receivedata_fine,headers=headers).text)
#                 allfine_data = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': '',
#                 'sendSiteName': '',
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': '',
#                 }
#                 item['allfineBusiDetailSummaryVo']=json.loads(requests.post(fhf_url,data=allfine_data,headers=headers).text)
#                 fin_data = {
#                 'isAll':'0',
#                 'page':'1',
#                 'pageSize':'50',
#                 # 'loginSiteType':'139',
#                 'loginSiteId':site_info['data']['siteId'],
#                 'radioDate':'0',
#                 'queryType':'1',
#                 'depositSiteId':'0',
#                 'siteId':'0',
#                 'accountType':'',
#                 'accountStatus':'1',
#                 'currentLoginSiteName':site_info['data']['siteName'],
#                 }
#                 item['finAccountList'] = json.loads(requests.post(finlist_url,data=fin_data,headers=headers).text)
#                 item['code'] = 200
#                 item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 print('**************************************')
#                 self.close()
#                 #print(item)
#                 end3 = datetime.datetime.now()
#                 print('总耗时:{}'.format(end3-sta))
#                 return item
#
#                 # return self.caiji()
#             else:
#                 #self.i+=1
#                 #print('*************'+str(self.i))
#                 #if self.i < 3:
#                 #   return self.crack_slider(username, password)
#                 self.close()
#                 error_msg = {
#                         "msg": "",
#                         "code": 600,
#                 }
#                 print('**************600*******************')
#                 return error_msg
#         except Exception as e:
#             print(e)
#             self.close()
#             error_msg = {
#                 "msg": "",
#                 "code": 600,
#             }
#             return error_msg
#     def close(self):
#         self.driver.quit()


# class CrackSlider():
#     def __init__(self):
#         super(CrackSlider, self).__init__()
#         self.url = 'http://fin.ane56.com/account/welcome'
#         chrome_options = Options()
#         chrome_options.add_argument("window-size=1920,1080")
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--start-maximized")
#         self.driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1',options=chrome_options)
#         self.wait = WebDriverWait(self.driver,0.3)
#         self.zoom = 1
#         #self.i = 0
#
#     def open(self):
#         self.driver.get(self.url)
#
#     def get_pic(self):
#         time.sleep(2)
#         target = self.driver.find_element_by_css_selector('#slide > div > div.validate_main > img.validate_big')
#         target.screenshot('target.jpg')
#         pic = cv2.imread('target.jpg')
#         pic = cv2.resize(pic, (600, 326), interpolation=cv2.INTER_CUBIC)
#         cv2.imwrite('target.jpg',pic)
#         local_img = Image.open('target.jpg')
#         size_loc = local_img.size
#         print(local_img.size)
#         self.zoom = 300 / int(size_loc[0])
#     def get_tracks(self, distance):
#         print(distance)
#         distance += 20
#         v = 0
#         t = 0.2
#         forward_tracks = []
#         current = 0
#         mid = distance * 3 / 5
#         while current < distance:
#             if current < mid:
#                 a = 2
#             else:
#                 a = -3
#             s = v * t + 0.5 * a * (t ** 2)
#             v = v + a * t
#             current += s
#             forward_tracks.append(round(s))
#
#         back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
#         return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}
#
#     def match(self, target, template,username,password):
#         #try:
#             #template = 'qk3.png'
#             img_rgb = cv2.imread(target)
#             img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#             template = cv2.imread(template, 0)
#             run = 1
#             w, h = template.shape[::-1]
#             print(w, h)
#             res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#             # 使用二分法查找阈值的精确值
#             L = 0
#             R = 1
#             while run < 20:
#                 run += 1
#                 threshold = (R + L) / 2
#                 print(threshold)
#                 if threshold < 0:
#                     print('Error')
#                     return None
#                 loc = np.where(res >= threshold)
#                 print(len(loc[1]))
#                 if len(loc[1]) > 1:
#                     L += (R - L) / 2
#                 elif len(loc[1]) == 1:
#                     print('目标区域起点x坐标为：%d' % loc[1][0])
#                     break
#                 elif len(loc[1]) < 1:
#                     R -= (R - L) / 2
#             print(loc)
#             return loc[1][0]
#         #except Exception as e:
#             #print(e)
#             #return self.crack_slider(username,password)
#     def crack_slider(self, username, password):
#         sta = datetime.datetime.now()
#         self.open()
#         end_wb = datetime.datetime.now()
#         print('网页访问时间'+str(end_wb-sta))
#         target = 'target.jpg'
#         template = '/home/xihonglin/Flask/SiteCrawlApi1.0/Spiders/qk3.png'
#         self.get_pic()
#         distance = self.match(target, template,username,password)
#         tracks = self.get_tracks((distance + 7) * self.zoom)  # 对位移的缩放计算
#         end = datetime.datetime.now()
#         print('验证码图片对比处理耗时:'+str(end-sta))
#         try:
#             slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'validate_button_icon')))
#             ActionChains(self.driver).click_and_hold(slider).perform()
#
#             for track in tracks['forward_tracks']:
#                 ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
#
#             # time.sleep(0.5)
#             for back_tracks in tracks['back_tracks']:
#                 ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()
#
#             ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
#             ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
#             # time.sleep(0.5)
#             ActionChains(self.driver).release().perform()
#             #time.sleep(1.8)
#             # time.sleep(0.6)
#             end = datetime.datetime.now()
#             print('验证码处理总耗时:'+str(end-sta))
#             self.driver.find_element_by_id('username').clear()
#             self.driver.find_element_by_id('username').send_keys(username)
#             self.driver.find_element_by_id('password').clear()
#             self.driver.find_element_by_id('password').send_keys(password)
#             time.sleep(0.3)
#             self.driver.find_element_by_css_selector(
#                 '#form > div.login_box_row.login_box_button > input.btn-submit').click()
#             time.sleep(0.6)
#             content = etree.HTML(self.driver.page_source)
#             title = content.xpath('//title/text()')[0]
#             if title == '欢迎页 - 统一结算平台':
#                 print('系统登录成功')
#                 end1 = datetime.datetime.now()
#                 print('系统登录耗时:'+str(end1-sta))
#                 mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
#                 jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
#                 jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1'
#                 accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
#                 code_url = 'http://api2.sz789.net:88/RecvByte.ashx'
#                 aut_url = 'https://fin.ane56.com/account/api/access/auth'
#                 users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
#                 fhf_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiDetailSummaryVo'
#                 finlist_url = 'https://fin.ane56.com/account/api/financeAccountMgr/queryFinAccountList'
#                 cookie = json.dumps(self.driver.get_cookies())
#                 cookie_dict = json.loads(cookie)
#                 cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
#                 cookies = '; '.join(item for item in cookie_list)
#                 headers = {
#                     'Accept': 'application/json',
#                     'Accept-Encoding': 'gzip, deflate, br',
#                     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#                     'Connection': 'keep-alive',
#                     'Content-Length': '0',
#                     'Content-Type': 'application/x-www-form-urlencoded',
#                     'Cookie': cookies,
#                     'Host': 'fin.ane56.com',
#                     'Origin': 'https://fin.ane56.com',
#                     'Referer': 'https://fin.ane56.com/account/welcome',
#                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
#                 }
#                 year = datetime.datetime.now().year
#                 month = datetime.datetime.now().month
#                 data = {
#                     'siteId': '',
#                 }
#                 item = {}
#                 # 网点基本信息
#                 site_info = json.loads(requests.post(aut_url, headers=headers).text)
#                 item['site_name'] = site_info['data']['siteName']
#                 item['site_id'] = site_info['data']['siteId']
#                 item['site_type'] = site_info['data']['siteVO']['siteTypeName']
#                 # 网点用户授权
#                 user_data = {
#                     "code": "",
#                     "name": "",
#                     "userRole": "",
#                     "status": "N",
#                     "page": "1",
#                     "pageSize": "50",
#                     "deptid": item['site_id'],
#                 }
#                 getUsers_info = json.loads(requests.post(users_url, data=user_data, headers=headers).text)
#                 item['getUser'] = getUsers_info
#                 # 年经营情况
#                 # print('网点年经营情况:')
#                 jr_qk = json.loads(requests.post(mjy_url, data=data, headers=headers).text)
#                 item['BusiDetailByMonth'] = jr_qk['data']
#
#                 # 交易费用汇总(昨日)
#                 # print('交易费用汇总:')
#                 jy_fyhz = json.loads(requests.post(jyxy_url, headers=headers).text)
#                 item['yesterdayBusiQuery'] = jy_fyhz['data']
#                 # 交易费用汇总(本月截止昨日)
#                 jy_fyhzyj = json.loads(requests.post(jyhzy_url, headers=headers).text)
#                 item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
#                 # 网点当前余额
#                 # print('网点当前余额:')
#                 accountinfo = json.loads(requests.post(accountinfo_url, headers=headers).text)
#                 item['AccountInfo'] = accountinfo
#                 #网点近一年发货费
#                 import calendar
#                 monthRange = calendar.monthrange(year,month-1)
#                 monthRange = monthRange[1]
#                 print(monthRange)
#                 data_send = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime':'{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': site_info['data']['siteName'],
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType':'',
#                 'parentChargeItemId':'176',
#                 }
#                 item['sendBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=data_send,headers=headers).text)
#                 data_receive={
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': '',
#                 'signSiteId': site_info['data']['siteId'],
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': site_info['data']['siteName'],
#                 }
#                 #item['receiveBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=data_receive,headers=headers).text)
#                 senddata_fine = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime':'{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': site_info['data']['siteId'],
#                 'sendSiteName': site_info['data']['siteName'],
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': '',
#                 }
#                 item['sendfineBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=senddata_fine,headers=headers).text)
#                 receivedata_fine = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '30',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': '',
#                 'sendSiteName': '',
#                 'signSiteId': site_info['data']['siteId'],
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': site_info['data']['siteName'],
#                 }
#                 item['receivefineBusiDetailSummaryVo'] = json.loads(requests.post(fhf_url,data=receivedata_fine,headers=headers).text)
#                 allfine_data = {
#                 'page': '1',
#                 'pageSize': '50',
#                 'bol': '0',
#                 'loginSiteId': '',
#                 'isEwbNo': 'false',
#                 'orderNos': '',
#                 'radioDate': '0',
#                 'isFill': 'false',
#                 'isFillNo': 'false',
#                 'startTime': '{}/{}/1 00:00:00'.format(year-1,month),
#                 'endTime': '{}/{}/{} 23:59:59'.format(year,month-1,monthRange),
#                 'accountId': '',
#                 'depositSiteId': '1617',
#                 'depositSiteName': '直营财务中心',
#                 'siteId': site_info['data']['siteId'],
#                 'siteName': site_info['data']['siteName'],
#                 'siteId1': '0',
#                 'siteName1': '',
#                 'accountType': '10',
#                 'accountStatus': '',
#                 'hedgeFlag': '',
#                 'transactionType': '',
#                 'chargeItemId': '101',
#                 'validFlag': '',
#                 'dataSource': '',
#                 'sendSiteId': '',
#                 'sendSiteName': '',
#                 'signSiteId': '',
#                 'signSiteName': '',
#                 'firstDeposit[siteId]':'1617',
#                 'firstDeposit[siteName]':'直营财务中心',
#                 'firstSite[siteName]':site_info['data']['siteName'],
#                 'firstSite[siteId]':site_info['data']['siteId'],
#                 'ewbNoType': '',
#                 'singSiteName': '',
#                 }
#                 item['allfineBusiDetailSummaryVo']=json.loads(requests.post(fhf_url,data=allfine_data,headers=headers).text)
#                 fin_data = {
#                 'isAll':'0',
#                 'page':'1',
#                 'pageSize':'50',
#                 # 'loginSiteType':'139',
#                 'loginSiteId':site_info['data']['siteId'],
#                 'radioDate':'0',
#                 'queryType':'1',
#                 'depositSiteId':'0',
#                 'siteId':'0',
#                 'accountType':'',
#                 'accountStatus':'1',
#                 'currentLoginSiteName':site_info['data']['siteName'],
#                 }
#                 item['finAccountList'] = json.loads(requests.post(finlist_url,data=fin_data,headers=headers).text)
#                 item['code'] = 200
#                 item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 print('**************************************')
#                 self.close()
#                 #print(item)
#                 end3 = datetime.datetime.now()
#                 print('总耗时:{}'.format(end3-sta))
#                 return item
#
#                 # return self.caiji()
#             else:
#                 #self.i+=1
#                 #print('*************'+str(self.i))
#                 #if self.i < 3:
#                 #   return self.crack_slider(username, password)
#                 self.close()
#                 error_msg = {
#                         "msg": "",
#                         "code": 600,
#                 }
#                 print('**************600*******************')
#                 return error_msg
#         except Exception as e:
#             print(e)
#             self.close()
#             error_msg = {
#                 "msg": "",
#                 "code": 600,
#             }
#             return error_msg
#     def close(self):
#         self.driver.quit()
