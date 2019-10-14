from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

import re
import cv2
import numpy as np
from io import BytesIO
import time, requests
from lxml import etree
import json
import datetime
import calendar
import threading

gLock = threading.Lock()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
monthRange = calendar.monthrange(year, month - 1)
monthRange = monthRange[1]


FORMAT = "%d-%d-%d"
year = datetime.datetime.now().year
month = datetime.datetime.now().month
date_list1 = []
date_list6 = []
for m in range(1, month):
    d = calendar.monthrange(year, m)
    date_list1.append(FORMAT % (year, m, d[1]))
    date_list6.append(FORMAT % (year, m, 1))
date_list3 = []
date_list9 = []
for n in range(month, 13):
    d = calendar.monthrange(year - 1, n)
    date_list3.append(FORMAT % (year - 1, n, d[1]))
    date_list9.append(FORMAT % (year-1, n, 1))
datesta_list = date_list6 + date_list9
dateend_list = date_list1 + date_list3
cookies_item = {}
class CrackSlider():
    def __init__(self):
        super(CrackSlider, self).__init__()
        self.url = 'https://lb.ane56.com/apps/index.zul'
        chrome_options = Options()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 3)
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
            s = v * t + 0.5 * a * (t ** 2)
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
        self.get_pic()
        target = 'target.jpg'
        template = '/home/xihonglin/Flask/testSiteCrawlApi/qk3.png'
        distance = self.match(target, template, username, password)
        tracks = self.get_tracks((distance + 7) * self.zoom)  # 对位移的缩放计算
        print(tracks)
        end = datetime.datetime.now()
        print('验证码图片对比处理耗时:' + str(end - sta))
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
            self.driver.get_screenshot_as_file('web3.png')
            time.sleep(0.6)
            end = datetime.datetime.now()
            print('验证码处理总耗时:' + str(end - sta))
            self.driver.find_element_by_id('username').clear()
            self.driver.find_element_by_id('username').send_keys(username)
            self.driver.find_element_by_id('password').clear()
            self.driver.find_element_by_id('password').send_keys(password)
            time.sleep(0.3)
            self.driver.find_element_by_css_selector(
                '#form > div.login_box_row.login_box_button > input.btn-submit').click()
            time.sleep(1)
            self.driver.get_screenshot_as_file('web6.png')
            content = etree.HTML(self.driver.page_source)
            keyword = content.xpath("//div[@class='z-div']/a/text()")
            print(keyword)
            if keyword != [] and keyword[0]=='丞风智能':
                print(keyword[0])
                print('系统登录成功')
                # cookies_list = json.dumps(self.driver.get_cookies())
                cookies = json.dumps(self.driver.get_cookies())
                cookie_dictlb = json.loads(cookies)
                cookie_listlb = [item["name"] + "=" + item["value"] for item in cookie_dictlb]
                cookies_lb = '; '.join(item for item in cookie_listlb)
                time.sleep(0.6)
                self.driver.get('http://fin.ane56.com/account/welcome')
                time.sleep(1.8)
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
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                }
                # cookies_item['cookies_list'] = cookies_list
                cookies_item['cookies_lb'] = cookies_lb
                cookies_item['jscookies'] = headers
                cookies_item['code'] = 0
                self.driver.quit()
                return cookies_item
            else:
                print("登录失败")
                self.driver.quit()
                cookies_item['code'] = 1
                return cookies_item
        except Exception as e:
            self.driver.quit()
            print(e)
            cookies_item['code'] = 1
            return cookies_item



# def crawl(n):
#     # desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
#     # desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
#     chrome_options = Options()
#     chrome_options.add_argument("window-size=1920,1080")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(r'/Users/honglin/Downloads/chromedriver',options=chrome_options)
#     driver.implicitly_wait(10)
#     print(cookies_item['cookies_list'])
#     list_cookies = json.loads(cookies_item['cookies_list'])
#     try:
#         driver.get('https://lb.ane56.com/apps/index.zul')
#         driver.delete_all_cookies()
#         for cookie in list_cookies:
#             driver.add_cookie({
#                 'domain': cookie['domain'],  # 此处xxx.com前，需要带点
#                 'name': cookie['name'],
#                 'value': cookie['value'],
#                 'path': cookie['path'],
#                 'expires': None
#             })
#         driver.get('https://lb.ane56.com/apps/index.zul')
#         time.sleep(1)
#         driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[4]").click()
#         time.sleep(1)
#         driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[6]").click()
#         time.sleep(1)
#         driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[8]").click()
#         time.sleep(3)
#         list_yw = []
#         driver.get_screenshot_as_file('web3.png')
#         for i in range(n, n+3):
#             item = {}
#             item['date'] = datesta_list[i]
#             driver.find_element_by_xpath("//td[2]//i[@class='required z-datebox']/input").clear()
#             driver.find_element_by_xpath("//td[2]//i[@class='required z-datebox']/input").send_keys(datesta_list[i])
#             driver.find_element_by_xpath("//td[3]/div/i[@class='required z-datebox']/input").clear()
#             driver.find_element_by_xpath("//td[3]/div/i[@class='required z-datebox']/input").send_keys(
#                 dateend_list[i])
#             driver.find_element_by_xpath("//tr[@valign='middle']/td[1]/button").click()
#             time.sleep(7)
#             content = etree.HTML(driver.page_source)
#             try:
#                 item['p_num'] = content.xpath("//tr[@valign='middle']/td[3]/span/text()")[0]
#             except:
#                 item['p_num'] = ''
#             try:
#                 item['j_num'] = content.xpath("//tr[@valign='middle']/td[7]/span/text()")[0]
#             except:
#                 item['j_num'] = ''
#             try:
#                 item['js_width'] = content.xpath("//tr[@valign='middle']/td[11]/span/text()")[0]
#             except:
#                 item['js_width'] = ''
#             try:
#                 item['sj_width'] = content.xpath("//tr[@valign='middle']/td[15]/span/text()")[0]
#             except:
#                 item['sj_width'] = ''
#             try:
#                 item['zz_width'] = content.xpath("//tr[@valign='middle']/td[19]/span/text()")[0]
#             except:
#                 item['zz_width'] = ''
#             try:
#                 item['tj_'] = content.xpath("//tr[@valign='middle']/td[23]/span/text()")[0]
#             except:
#                 item['tj_'] = ' '
#             try:
#                 item['dfk'] = content.xpath("//tr[@valign='middle']/td[27]/span/text()")[0]
#             except:
#                 item['dfk'] = ''
#             try:
#                 item['xj_'] = content.xpath("//tr[@valign='middle']/td[31]/span/text()")[1]
#             except:
#                 item['xj_'] = ''
#             try:
#                 item['yj'] = content.xpath("//tr[@valign='middle']/td[35]/span/text()")[1]
#             except:
#                 item['yj'] = ''
#             try:
#                 item['yf_hj'] = content.xpath("//tr[@valign='middle']/td[39]/span/text()")[0]
#             except:
#                 item['yf_hj'] = ''
#             list_yw.append(item)
#         driver.quit()
#         return list_yw
#     except Exception as e:
#         print(e)
#         driver.quit()
#     finally:
#         driver.quit()
#
#
item = {}
# yw_list = []
# class A(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#        yw_list.extend(crawl(0))
#
#
# class B(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         yw_list.extend(crawl(3))
#
#
# class C(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         yw_list.extend(crawl(6))
#
#
# class D(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         yw_list.extend(crawl(9))
#         item_all['yw_list'] = yw_list

class K(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        index_url = 'https://lb.ane56.com/apps/index.zul'
        url = 'https://lb.ane56.com/ne1/basedata/site_query_area.zul'
        zk_url = 'https://lb.ane56.com/zkau'
        headers = {
            'Cookie':cookies_item['cookies_lb'],
        }

        index_r = requests.get(index_url, headers=headers).text

        sitename_body = "{id:'labEmployeeSite',style:'color:white',value:'(.*?)'}"
        sitename_pattern = re.compile(sitename_body)
        sitename = re.findall(sitename_pattern, index_r)[0].strip(r'\u3010  \u3011')
        print(sitename)
        print(len(sitename))

        home_r = requests.get(url, headers=headers).text

        dtid_body = "{id:'pg_site_area_query',dt:'(.*?)'"
        pattern_dtid = re.compile(dtid_body)
        dtid_code = re.findall(pattern_dtid, home_r)[0]

        body_input = "'zul.inp.Textbox','(.*?)',{id:'txtSiteName'"
        pattern_inp = re.compile(body_input)
        inp_code = re.findall(pattern_inp, home_r)[0]

        search_body = "'zul.wgt.Button','(.*?)',{id:'btnSeach'"
        pattern_search = re.compile(search_body)
        search_code = re.findall(pattern_search, home_r)[0]

        print(dtid_code)
        print(inp_code)
        print(search_code)

        headers1 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '156',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookies_item['cookies_lb'],
            'Host': 'lb.ane56.com',
            'Origin': 'https://lb.ane56.com',
            'Referer': 'https://lb.ane56.com/apps/index.zul',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid),
        }

        data_1 = {
            'dtid': dtid_code,
            'cmd_0': 'onChanging',
            'opt_0': 'i',
            'uuid_0': inp_code,
            'data_0': '{"value":'+'"'+sitename+'"'+',"start":'+str(len(sitename))+'}',
        }

        alert_r = requests.post(zk_url, data=data_1, headers=headers1).text

        alert_body = r"'zul.wnd.Window','(.*?)'"
        pattern_alert = re.compile(alert_body)
        alert_code = re.findall(pattern_alert, alert_r)[0]
        print(alert_code)

        headers2 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '335',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookies_item['cookies_lb'],
            'Host': 'lb.ane56.com',
            'Origin': 'https://lb.ane56.com',
            'Referer': 'https://lb.ane56.com/ne1/basedata/site_query_area.zul',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1),
        }
        data_2 = {
            'dtid': dtid_code,
            'cmd_0': 'onMove',
            'opt_0': 'i',
            'uuid_0': alert_code,
            'data_0': '{"left":"615px","top":"56px"}',
            'cmd_1': 'onZIndex',
            'opt_1': 'i',
            'uuid_1': alert_code,
            'data_1': '{"":1800}',
            'cmd_2': 'onChange',
            'uuid_2': inp_code,
            'data_2': '{"value":'+'"'+sitename+'"'+',"start":'+str(len(sitename))+'}',
            'cmd_3': 'onBlur',
            'uuid_3': inp_code,
        }

        inp_r = requests.post(zk_url, data=data_2, headers=headers2).text
        # print(inp_r)

        headers3 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '133',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookies_item['cookies_lb'],
            'Host': 'lb.ane56.com',
            'Origin': 'https://lb.ane56.com',
            'Referer': 'https://lb.ane56.com/ne1/basedata/site_query_area.zul',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1 + 1),
        }
        data_3 = {
            'dtid': dtid_code,
            'cmd_0': 'onClick',
            'uuid_0': search_code,
            'data_0': '{"pageX":40,"pageY":8,"which":1,"x":33,"y":6}',
        }

        siteinfo_r = requests.post(zk_url, data=data_3, headers=headers3).text

        # print(siteinfo_r)

        siteinfo_body = '{label:"(.*?)"}'
        siteinfo_pattern = re.compile(siteinfo_body)
        siteinfo_list = re.findall(siteinfo_pattern, siteinfo_r)
        # print(siteinfo_list)
        print(siteinfo_list[4])
        print(siteinfo_list[5])
        gLock.acquire()
        item['user'] = siteinfo_list[4]
        item['phone'] = siteinfo_list[5]
        gLock.release()


        # desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        # desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        # chrome_options = Options()
        # chrome_options.add_argument("window-size=1920,1080")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--start-maximized")
        # driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        # print(cookies_item['cookies_list'])
        # list_cookies = json.loads(cookies_item['cookies_list'])
        # try:
        #     driver.get('https://lb.ane56.com/apps/index.zul')
        #     driver.delete_all_cookies()
        #     for cookie in list_cookies:
        #         driver.add_cookie({
        #             'domain': cookie['domain'],  # 此处xxx.com前，需要带点
        #             'name': cookie['name'],
        #             'value': cookie['value'],
        #             'path': cookie['path'],
        #             'expires': None
        #         })
        #     time.sleep(1.2)
        #     driver.get('https://lb.ane56.com/apps/index.zul')
        #     driver.get_screenshot_as_file('web.png')
        #     time.sleep(1.8)
        #     sitename = etree.HTML(driver.page_source).xpath("//td[37]/span/text()")[0].strip("【 】")
        #     print(sitename)
        #     time.sleep(1.8)
        #     driver.find_element_by_xpath("//tr[1]//td//div[@class='z-treecell-cnt z-overflow-hidden']").click()
        #     time.sleep(0.6)
        #     driver.find_element_by_xpath("//tr[4]//td//div[@class='z-treecell-cnt z-overflow-hidden']/span[1]").click()
        #     time.sleep(3)
        #     driver.find_element_by_xpath("//table[@class='z-tablelayout'][1]//tr[2]/td[2]/div[1]/input").send_keys(
        #         sitename)
        #     time.sleep(3)
        #     driver.find_element_by_xpath("//div[@class='z-toolbar-body z-toolbar-start']/button").click()
        #     time.sleep(3)
        #     user_content = etree.HTML(driver.page_source)
        #     gLock.acquire()
        #     item['user'] = user_content.xpath("//tr/td[8]/div/text()")[0]
        #     item['phone'] = user_content.xpath("//tr/td[9]/div/text()")[0]
        #     gLock.release()
        # except Exception as e:
        #     print(e)
        #     print('***********')
        # finally:
        #     driver.quit()


mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1'
accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
code_url = 'http://api2.sz789.net:88/RecvByte.ashx'
aut_url = 'https://fin.ane56.com/account/api/access/auth'
users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
fhf_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiDetailSummaryVo'
finlist_url = 'https://fin.ane56.com/account/api/financeAccountMgr/queryFinAccountList'


# 用户权限列表
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=cookies_item['jscookies']).text)
        gLock.acquire()
        item['site_name'] = site_info['data']['siteVO']['siteName']
        item['site_id'] = site_info['data']['siteVO']['siteId']
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
        getUsers_info = json.loads(requests.post(users_url, data=user_data, headers=cookies_item['jscookies']).text)
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
        jr_qk = json.loads(requests.post(mjy_url, data=data, headers=cookies_item['jscookies']).text)
        gLock.acquire()
        item['BusiDetailByMonth'] = jr_qk['data']
        gLock.release()


# 交易费用汇总(昨日)
class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        jy_fyhz = json.loads(requests.post(jyxy_url, headers=cookies_item['jscookies']).text)
        gLock.acquire()
        item['yesterdayBusiQuery'] = jy_fyhz['data']
        gLock.release()


# 交易费用汇总(本月截止昨日)
class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        jy_fyhzyj = json.loads(requests.post(jyhzy_url, headers=cookies_item['jscookies']).text)
        gLock.acquire()
        item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
        gLock.release()


# 网点当前余额
class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        accountinfo = json.loads(requests.post(accountinfo_url, headers=cookies_item['jscookies']).text)
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
        site_info = json.loads(requests.post(aut_url, headers=cookies_item['jscookies']).text)
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
            'siteId': site_info['data']['siteVO']['siteId'],
            'siteName': site_info['data']['siteVO']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': site_info['data']['siteVO']['siteId'],
            'sendSiteName': site_info['data']['siteVO']['siteName'],
            'signSiteId': '',
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteVO']['siteName'],
            'firstSite[siteId]': site_info['data']['siteVO']['siteId'],
            'ewbNoType': '',
            'parentChargeItemId': '176',
        }
        gLock.acquire()
        item['sendBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=data_send, headers=cookies_item['jscookies']).text)
        gLock.release()


# 罚款(寄件网点)
class H(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=cookies_item['jscookies']).text)
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
            'siteId': site_info['data']['siteVO']['siteId'],
            'siteName': site_info['data']['siteVO']['siteName'],
            'siteId1': '0',
            'siteName1': '',
            'accountType': '10',
            'accountStatus': '',
            'hedgeFlag': '',
            'transactionType': '',
            'chargeItemId': '101',
            'validFlag': '',
            'dataSource': '',
            'sendSiteId': site_info['data']['siteVO']['siteId'],
            'sendSiteName': site_info['data']['siteVO']['siteName'],
            'signSiteId': '',
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteVO']['siteName'],
            'firstSite[siteId]': site_info['data']['siteVO']['siteId'],
            'ewbNoType': '',
            'singSiteName': '',
        }
        gLock.acquire()
        item['sendfineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=senddata_fine, headers=cookies_item['jscookies']).text)
        gLock.release()


# 罚款(签收网点)
class I(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=cookies_item['jscookies']).text)
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
            'siteId': site_info['data']['siteVO']['siteId'],
            'siteName': site_info['data']['siteVO']['siteName'],
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
            'signSiteId': site_info['data']['siteVO']['siteId'],
            'signSiteName': '',
            'firstDeposit[siteId]': '1617',
            'firstDeposit[siteName]': '直营财务中心',
            'firstSite[siteName]': site_info['data']['siteVO']['siteName'],
            'firstSite[siteId]': site_info['data']['siteVO']['siteId'],
            'ewbNoType': '',
            'singSiteName': site_info['data']['siteVO']['siteName'],
        }
        gLock.acquire()
        item['receivefineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=receivedata_fine, headers=cookies_item['jscookies']).text)
        gLock.release()


# 罚款(1级+2级)
class J(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        site_info = json.loads(requests.post(aut_url, headers=cookies_item['jscookies']).text)
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
            'siteId': site_info['data']['siteVO']['siteId'],
            'siteName': site_info['data']['siteVO']['siteName'],
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
            'firstSite[siteName]': site_info['data']['siteVO']['siteName'],
            'firstSite[siteId]': site_info['data']['siteVO']['siteId'],
            'ewbNoType': '',
            'singSiteName': '',
        }
        gLock.acquire()
        item['allfineBusiDetailSummaryVo'] = json.loads(
            requests.post(fhf_url, data=allfine_data, headers=cookies_item['jscookies']).text)
        gLock.release()


def lb_spider(username,password):
    c = CrackSlider()
    cookies_item = c.crack_slider(username,password)
    if cookies_item['code'] == 0:
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
        t10 = K()
        t10.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        return item
    else:
        return {"msg":"",
                "code":600}

# sta = time.time()
# print(lb_spider('5563015', 'ane1112223.'))
# end = time.time()
# print(end-sta)



        #         item_all = {}
        #         self.driver.find_element_by_xpath("//tr[1]//td//div[@class='z-treecell-cnt z-overflow-hidden']").click()
        #         time.sleep(0.6)
        #         self.driver.find_element_by_xpath("//tr[4]//td//div[@class='z-treecell-cnt z-overflow-hidden']/span[1]").click()
        #         time.sleep(3)
        #         self.driver.find_element_by_xpath("//table[@class='z-tablelayout'][1]//tr[2]/td[2]/div[1]/input").send_keys("安徽桐城文都")
        #         time.sleep(3)
        #         self.driver.find_element_by_xpath("//div[@class='z-toolbar-body z-toolbar-start']/button").click()
        #         time.sleep(3)
        #         user_content = etree.HTML(self.driver.page_source)
        #         item_all['user'] = user_content.xpath("//tr/td[8]/div/text()")[0]
        #         item_all['phone'] = user_content.xpath("//tr/td[9]/div/text()")[0]
        #         print(item_all)
        #         self.driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[14]").click()
        #         time.sleep(0.3)
        #         self.driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[16]").click()
        #         time.sleep(0.3)
        #         self.driver.find_element_by_xpath("//div[@class='z-tree-body']//tr[18]").click()
        #         time.sleep(3)
        #         # self.driver.find_element_by_xpath("//tr[@valign ='middle']//tr/td[17]").click()
        #         yw_list = []
        #         for i in range(0, 12):
        #             item = {}
        #             item['date'] = datesta_list[i]
        #             self.driver.find_element_by_xpath("//td[2]//i[@class='required z-datebox']/input").clear()
        #             self.driver.find_element_by_xpath("//td[2]//i[@class='required z-datebox']/input").send_keys(
        #                 datesta_list[i])
        #             self.driver.find_element_by_xpath("//td[3]/div/i[@class='required z-datebox']/input").clear()
        #             self.driver.find_element_by_xpath("//td[3]/div/i[@class='required z-datebox']/input").send_keys(
        #                 dateend_list[i])
        #             self.driver.find_element_by_xpath("//tr[@valign='middle']/td[1]/button").click()
        #             time.sleep(7)
        #             content = etree.HTML(self.driver.page_source)
        #             try:
        #                 item['p_num'] = content.xpath("//tr[@valign='middle']/td[3]/span/text()")[0]
        #             except:
        #                 item['p_num'] = ''
        #             try:
        #                 item['j_num'] = content.xpath("//tr[@valign='middle']/td[7]/span/text()")[0]
        #             except:
        #                 item['j_num'] = ''
        #             try:
        #                 item['js_width'] = content.xpath("//tr[@valign='middle']/td[11]/span/text()")[0]
        #             except:
        #                 item['js_width'] = ''
        #             try:
        #                 item['sj_width'] = content.xpath("//tr[@valign='middle']/td[15]/span/text()")[0]
        #             except:
        #                 item['sj_width'] = ''
        #             try:
        #                 item['zz_width'] = content.xpath("//tr[@valign='middle']/td[19]/span/text()")[0]
        #             except:
        #                 item['zz_width'] = ''
        #             try:
        #                 item['tj_'] = content.xpath("//tr[@valign='middle']/td[23]/span/text()")[0]
        #             except:
        #                 item['tj_'] = ' '
        #             try:
        #                 item['dfk'] = content.xpath("//tr[@valign='middle']/td[27]/span/text()")[0]
        #             except:
        #                 item['dfk'] = ''
        #             try:
        #                 item['xj_'] = content.xpath("//tr[@valign='middle']/td[31]/span/text()")[1]
        #             except:
        #                 item['xj_'] = ''
        #             try:
        #                 item['yj'] = content.xpath("//tr[@valign='middle']/td[35]/span/text()")[1]
        #             except:
        #                 item['yj'] = ''
        #             try:
        #                 item['yf_hj'] = content.xpath("//tr[@valign='middle']/td[39]/span/text()")[0]
        #             except:
        #                 item['yf_hj'] = ''
        #             yw_list.append(item)
        #         item_all['yw_list'] = yw_list
        #         print(item_all)
        #         # self.caiji()
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         self.driver.quit()
        # else:
        #     self.driver.quit()


if __name__ == '__main__':
    sta = time.time()
    c = CrackSlider()
    print(lb_spider('8983027','gangao54321$'))
    end = time.time()
    print(end-sta)
