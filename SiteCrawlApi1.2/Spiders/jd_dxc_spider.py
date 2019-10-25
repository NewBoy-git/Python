import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import json
import datetime
import calendar
import binascii
import requests
from lxml import etree
# from HbaseHandler.operateHbase import save_to_hbase

import threading

from flask import Flask


item_all = {}
ztList = []
yjztList = []
gLock = threading.Lock()


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
# print(datesta_list)
# print(dateend_list)

# print(driver.page_source)
def jd_login(username,password):
    cookie_item = {}
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,983")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        # driver.implicity_wait(10)
        # wait = WebDriverWait(driver, 10)  #后面可以使用wait对特定元素进行等待
        # driver.get(url)
    try:
        url = 'http://sxne.sxjdfreight.com/common/login.zul'
        driver.get(url)
        time.sleep(3)
        jd_code = driver.find_element_by_class_name('z-image')
        jd_code.screenshot('jd_code.png')
        driver.find_element_by_class_name('z-textbox-focus').clear()
        driver.find_element_by_class_name('z-textbox-focus').send_keys(username)
        driver.find_element_by_name('j_password').clear()
        driver.find_element_by_name('j_password').send_keys(password)
        url = 'http://api2.sz789.net:88/RecvByte.ashx'
        f = open('jd_code.png', 'rb')
        a = f.read()
        hexstr = binascii.b2a_hex(a)
        data = {
            'username': 'hyjkjkj1009',
            'password': 'hyjkjkj1009',
            'softId': '67781',
            'imgdata': hexstr,
        }
        r = requests.post(url, data=data).text
        obj = json.loads(r)
        code = obj['result']
        driver.find_element_by_name('verificationCode').clear()
        driver.find_element_by_name('verificationCode').send_keys(code)
        button = driver.find_element_by_id('imgLogin')
        driver.execute_script("$(arguments[0]).click()", button)
        time.sleep(3)
        content1 = etree.HTML(driver.page_source)
        sitename = content1.xpath('//tr[@valign="middle"]/td[13]/span/text()')[0].strip("【  】")
        print(sitename)
        if sitename:
            cookie_list = json.dumps(driver.get_cookies())
            cookie_item['cookie_list'] = cookie_list
            cookie_item['code'] = 0
            cookie_item['sitename'] = sitename
            with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(cookie_item))
            driver.quit()
            return cookie_item
        else:
            cookie_item['code'] =1
            with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(cookie_item))
            driver.quit()
            return cookie_item
    except Exception as e:
        driver.quit()
        print(e)
        cookie_item['code'] = 1
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(cookie_item))
        return cookie_item


def crawl_zt(n):
    with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
                cookie_item = json.loads(f.read())
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,983")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
    list_cookie = json.loads(cookie_item['cookie_list'])
    # print(list_cookie)
    zt_list = []
    try:
        driver.get('http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul')
        driver.delete_all_cookies()
        for cookie in list_cookie:
            driver.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })
        driver.get('http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul')
        time.sleep(18)
        for i in range(n,n+3):
            zt_item = {}
            zt_item['date'] = datesta_list[i]
            driver.find_element_by_xpath("//td[3]//td[2]//i[@class='required z-datebox']/input").clear()
            driver.find_element_by_xpath("//td[3]//td[2]//i[@class='required z-datebox']/input").send_keys(datesta_list[i])
            driver.find_element_by_xpath("//td[3]//td[3]//i[@class='required z-datebox']/input").clear()
            driver.find_element_by_xpath("//td[3]//td[3]//i[@class='required z-datebox']/input").send_keys(dateend_list[i])
            driver.find_element_by_xpath('//tr[@valign="middle"]/td//td[1]/button').click()
            time.sleep(24)
            content = etree.HTML(driver.page_source)
            # item['ps'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[3]//text()")[0]
            # item['js'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[7]//text()")[0]
            try:
                zt_item['js_width'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[11]//text()")[0]
            except Exception as e:
                zt_item['js_width'] = ''
            try:
                zt_item['sendfree'] = content.xpath("//div[@class='z-div']/table[1]//tr[2]/td[2]//td[11]//text()")[0]
            except Exception as e:
                zt_item['sendfree'] = ''
            # print(zt_item)
            zt_list.append(zt_item)
        print(zt_list)
        driver.quit()
        return zt_list
    except Exception as e:
        print(e)
        driver.quit()
        return zt_list
    finally:
        driver.quit()
        return zt_list


def crawl_yj(n):
    with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
                cookie_item = json.loads(f.read())
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,983")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
    list_cookie = json.loads(cookie_item['cookie_list'])
    print(list_cookie)
    sitename = cookie_item['sitename']
    yjzt_list = []
    try:
        driver.get('http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul')
        driver.delete_all_cookies()
        for cookie in list_cookie:
            driver.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })
        driver.get('http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul')
        time.sleep(18)
        driver.find_element_by_xpath('//tr[2]/td[2]//input[@class="z-textbox"]').send_keys(sitename)
        time.sleep(1)
        for i in range(n, n + 3):
            zt_item = {}
            zt_item['date'] = datesta_list[i]
            driver.find_element_by_xpath("//td[3]//td[2]//i[@class='required z-datebox']/input").clear()
            driver.find_element_by_xpath("//td[3]//td[2]//i[@class='required z-datebox']/input").send_keys(
                datesta_list[i])
            driver.find_element_by_xpath("//td[3]//td[3]//i[@class='required z-datebox']/input").clear()
            driver.find_element_by_xpath("//td[3]//td[3]//i[@class='required z-datebox']/input").send_keys(
                dateend_list[i])
            driver.find_element_by_xpath('//tr[@valign="middle"]/td//td[1]/button').click()
            time.sleep(24)
            content = etree.HTML(driver.page_source)
            # item['ps'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[3]//text()")[0]
            # item['js'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[7]//text()")[0]
            try:
                zt_item['js_width'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[11]//text()")[0]
            except Exception as e:
                zt_item['js_width'] = ''
            try:
                zt_item['sendfree'] = content.xpath("//div[@class='z-div']/table[1]//tr[2]/td[2]//td[11]//text()")[0]
            except Exception as e:
                zt_item['sendfree'] = ''
            # print(zt_item)
            yjzt_list.append(zt_item)
        print(yjzt_list)
        driver.quit()
        return yjzt_list
    except Exception as e:
        print(e)
        driver.quit()
        return yjzt_list
    finally:
        driver.quit()


def crawl_pjf(n):
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
            cookie_item = json.loads(f.read())
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        chrome_options = Options()
        chrome_options.add_argument("window-size=1200,983")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        list_cookie = json.loads(cookie_item['cookie_list'])
        print(list_cookie)
        try:
            driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
            driver.delete_all_cookies()
            for cookie in list_cookie:
                driver.add_cookie({
                    'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': cookie['path'],
                    'expires': None
                })
            driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
            time.sleep(9)
            driver.find_elements_by_xpath('//div[@class="z-tabbox"][1]//div[@class="z-tabs z-tabs-scroll"]//div[@class="z-tabs-header"]//li[2]//span')[0].click()
            time.sleep(3)
            psf_list = []
            for i in range(n, n + 3):
                psf_item = {}
                psf_item['date'] = datesta_list[i]
                driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[2]/i[1]/input').clear()
                driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[2]/i[1]/input').send_keys(
                    datesta_list[i])
                driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[3]/i[1]/input').clear()
                driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[3]/i[1]/input').send_keys(
                    dateend_list[i])
                # print(driver.page_source)
                time.sleep(3)
                driver.find_element_by_xpath('//tr[6]/td[4]/div/input').clear()
                driver.find_element_by_xpath('//tr[6]/td[4]/div/input').send_keys("付派送费")
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/button[1]').click()
                # print(button)
                # driver.execute_script(
                #     "arguments[0].setAttribute('style', arguments[1]);",
                #     button,
                #     "border: 2px solid red;"  # 边框border:2px; red红色
                # )
                time.sleep(18)
                content = etree.HTML(driver.page_source)
                # item['ps'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[3]//text()")[0]
                # item['js'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[7]//text()")[0]
                try:
                    psf_item['psf'] = content.xpath('//div[@style="padding-top:2px;"]/span[2]/text()')[0]
                except Exception as e:
                    psf_item['psf'] = ''
                print(psf_item)
                psf_list.append(psf_item)
            print(psf_list)
            driver.quit()
            return psf_list
        except Exception as e:
            print(e)
            driver.quit()
        finally:
            driver.quit()


def crawl_ztpjf(n):
    with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
        cookie_item = json.loads(f.read())
    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,983")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
    list_cookie = json.loads(cookie_item['cookie_list'])
    print(list_cookie)
    try:
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
        driver.delete_all_cookies()
        for cookie in list_cookie:
            driver.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
        time.sleep(9)
        driver.find_elements_by_xpath(
            '//div[@class="z-tabbox"][1]//div[@class="z-tabs z-tabs-scroll"]//div[@class="z-tabs-header"]//li[2]//span')[
            0].click()
        time.sleep(3)
        psf_list = []
        for i in range(n, n + 3):
            psf_item = {}
            psf_item['date'] = datesta_list[i]
            driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[2]/i[1]/input').clear()
            driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[2]/i[1]/input').send_keys(
                datesta_list[i])
            driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[3]/i[1]/input').clear()
            driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//td[3]/i[1]/input').send_keys(
                dateend_list[i])
            # print(driver.page_source)
            time.sleep(3)
            driver.find_element_by_xpath('//tr[5]/td[6]/div/input').clear()
            driver.find_element_by_xpath('//tr[6]/td[4]/div/input').clear()
            driver.find_element_by_xpath('//tr[6]/td[4]/div/input').send_keys("付派送费")
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/button[1]').click()
            # print(button)
            # driver.execute_script(
            #     "arguments[0].setAttribute('style', arguments[1]);",
            #     button,
            #     "border: 2px solid red;"  # 边框border:2px; red红色
            # )
            time.sleep(18)
            content = etree.HTML(driver.page_source)
            # item['ps'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[3]//text()")[0]
            # item['js'] = content.xpath("//div[@class='z-div']/table[1]//tr[1]/td[2]//td[7]//text()")[0]
            try:
                psf_item['psf'] = content.xpath('//div[@style="padding-top:2px;"]/span[2]/text()')[0]
            except Exception as e:
                psf_item['psf'] = ''
            print(psf_item)
            psf_list.append(psf_item)
        print(psf_list)
        driver.quit()
        return psf_list
    except Exception as e:
        print(e)
        driver.quit()
    finally:
        driver.quit()


class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        chrome_options = Options()
        chrome_options.add_argument("window-size=1200,983")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)

        driver.get('http://sxne.sxjdfreight.com/apps/index.zul')
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
                cookie_item = json.loads(f.read())
        list_cookie = json.loads(cookie_item['cookie_list'])
        print(list_cookie)
        driver.delete_all_cookies()
        try:
            for cookie in list_cookie:
                driver.add_cookie({
                    'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': cookie['path'],
                    'expires': None
                })
            driver.get('http://sxne.sxjdfreight.com/apps/index.zul')
            time.sleep(6)
            sitename = cookie_item['sitename']
            print(sitename)
            driver.get_screenshot_as_file('jd_web1.png')
            driver.find_element_by_xpath('//table[@class="z-tablelayout"]//tr[3]//button').click()
            time.sleep(1)
            driver.find_element_by_xpath('//tbody[@class="z-treechildren"]/tr[2]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//tbody[@class="z-treechildren"]/tr[10]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//tr[2]/td[2]//input[@style="width:130px;"]').send_keys(sitename)
            time.sleep(3)
            driver.find_element_by_xpath('//div[@class="z-toolbar-body z-toolbar-start"]//button[1]').click()
            time.sleep(6)
            driver.get_screenshot_as_file('jd_web3.png')
            content3 = etree.HTML(driver.page_source)
            item_all['siteName'] = sitename
            item_all['siteType'] = content3.xpath('//table[@style="table-layout:fixed;"]//td[4]//text()')[0]
            item_all['siteStatus'] = content3.xpath('//table[@style="table-layout:fixed;"]//td[7]//text()')[0]
            item_all['user'] = content3.xpath('//td[7]/span/text()')[0].strip("【】")
            item_all['code'] = 0
            pho = driver.find_element_by_xpath("//div[@class='z-listbox-body']//td[2]/div")
            ActionChains(driver).double_click(pho).perform()
            time.sleep(3)
            content6 = etree.HTML(driver.page_source)
            item_all['phone'] = content6.xpath('//tr/td[1]/div/div[3]/div[3]/table/tbody/tr[2]/td[2]/div/input/@value')[
                0]
            driver.quit()
        except Exception as e:
            driver.quit()
            print('界面未登录')
            print(e)

class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
            cookie_item = json.loads(f.read())
        list_cookie = json.loads(cookie_item['cookie_list'])
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        chrome_options = Options()
        chrome_options.add_argument("window-size=1200,983")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul')
        driver.delete_all_cookies()
        for cookie in list_cookie:
            driver.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul')
        time.sleep(6)
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[1]/div[4]/div[3]/div/table/tbody/tr[2]/td[2]/div/div[1]/i/input').clear()
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[1]/div[4]/div[3]/div/table/tbody/tr[2]/td[2]/div/div[1]/i/input').send_keys(
                date_list9[0])
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[1]/div[4]/div[3]/div/table/tbody/tr[2]/td[2]/div/div[4]/i/input').clear()
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[1]/div[4]/div[3]/div/table/tbody/tr[2]/td[2]/div/div[4]/i/input').send_keys(
                date_list1[0])
            driver.find_element_by_xpath('//div[@class="z-toolbar-body z-toolbar-start"]//button[1]').click()
            time.sleep(18)
            content9 = etree.HTML(driver.page_source)
            # gLock.acquire()
            item_all['frCompany'] = content9.xpath('//div[@class="mini-grid-rows-content"]//td[4]/div/text()')[0]
            item_all['zcfk'] = content9.xpath('//div[@class="mini-grid-rows-content"]//td[24]/div/text()')[0]
            item_all['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item_all['code'] = 0
            # gLock.release()
            driver.quit()
        except Exception as e:
            driver.quit()
            print('页面未加载完成', e)

class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
            cookie_item = json.loads(f.read())
        list_cookie = json.loads(cookie_item['cookie_list'])
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        chrome_options = Options()
        chrome_options.add_argument("window-size=1200,983")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
        driver.delete_all_cookies()
        for cookie in list_cookie:
            driver.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })
        driver.get('http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul')
        time.sleep(6)
        content12 = etree.HTML(driver.page_source)
        try:
            # gLock.acquire()
            item_all['yfk'] = content12.xpath('//div[@class="mini-grid-rows-content"]/table//tr[3]/td[3]/div/text()')[0]
            # gLock.release()
            driver.quit()
        except Exception as e:
            print(e)
            driver.quit()

class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        ztList.clear()
        lis = crawl_zt(0)
        # gLock.acquire()
        ztList.extend(lis)
        # gLock.release()


class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_zt(3)
        # gLock.acquire()
        ztList.extend(lis)
        # gLock.release()


class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_zt(6)
        # gLock.acquire()
        ztList.extend(lis)
        # gLock.release()

class G(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_zt(9)
        ztList.extend(lis)
        # gLock.acquire()
        item_all['ztList'] = ztList
        # gLock.release()
        print(item_all)


class H(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        yjztList.clear()
        lis = crawl_yj(0)
        # gLock.acquire()
        yjztList.extend(lis)
        # gLock.release()

class I(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_yj(3)
        # gLock.acquire()
        yjztList.extend(lis)
        # gLock.release()

class J(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_yj(6)
        # gLock.acquire()
        yjztList.extend(lis)
        # gLock.release()

class K(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_yj(9)
        yjztList.extend(lis)
        # gLock.acquire()
        item_all['yjztList'] = yjztList
        # gLock.release()
        print(item_all)


psfList = []

class L(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        psfList.clear()
        lis = crawl_pjf(0)
        psfList.extend(lis)

class M(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_pjf(3)
        psfList.extend(lis)

class N(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_pjf(6)
        psfList.extend(lis)

class O(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_pjf(9)
        psfList.extend(lis)
        # gLock.acquire()
        item_all['psfList'] = psfList
        # gLock.release()


psfztList = []
class P(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        psfztList.clear()
        lis = crawl_ztpjf(0)
        psfztList.extend(lis)

class Q(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_ztpjf(3)
        psfztList.extend(lis)

class R(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_ztpjf(6)
        psfztList.extend(lis)

class S(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        lis = crawl_ztpjf(9)
        psfztList.extend(lis)
        # gLock.acquire()
        item_all['psfztList'] = psfztList
        # gLock.release()








def jd_spider(userid,company):
    # jd_login(username,password)
    with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/cookie.json', 'r', encoding='utf-8') as f:
        cookie_item = json.loads(f.read())
        print(cookie_item)
    if cookie_item['code'] == 0:
        t12 = L()
        t12.start()
        t13 = M()
        t13.start()
        t14 = N()
        t14.start()
        t15 = O()
        t15.start()
        time.sleep(36)
        t1 = A()
        t1.start()
        t2 = B()
        t2.start()
        t3 = C()
        t3.start()
        time.sleep(18)
        t4 = D()
        t4.start()
        t5 = E()
        t5.start()
        t6 = F()
        t6.start()
        t7 = G()
        t7.start()
        time.sleep(18)
        t8 = H()
        t8.start()
        t9 = I()
        t9.start()
        t10 = J()
        t10.start()
        t11 = K()
        t11.start()

        t12.join()
        t13.join()
        t14.join()
        t15.join()
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
        t11.join()
        print('*************************************')
        item_all['userid'] = userid
        item_all['company'] = company
        # print(item_all)
        return item_all
    else:
        print({'msg':'','code':600})
        return {'msg':'','code':600}

if __name__ == '__main__':
    sta = datetime.datetime.now()
    item = jd_spider('18088664','sx201809.')
    print(item)
    end = datetime.datetime.now()
    print(end-sta)


