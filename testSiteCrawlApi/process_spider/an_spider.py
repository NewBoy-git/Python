from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import json
import requests
import warnings
warnings.filterwarnings('ignore')
import datetime
from lxml import etree


def login_an(username,password):
    url = 'http://fin.ane56.com/account/welcome'
    jyhzy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=1' 
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1',options=opt)
    driver.get(url)
    time.sleep(0.3)

    capimg = driver.find_element_by_id('cimg')


    capimg.screenshot("test_code.png")


    import binascii
    url = 'http://api2.sz789.net:88/RecvByte.ashx'

    f = open('test_code.png','rb')
    a = f.read()
    hexstr = binascii.b2a_hex(a)
    data = {
    'username':'hyjkjkj1009',
    'password':'hyjkjkj1009',
    'softId':'67781',
    'imgdata':hexstr,
    }

    r = requests.post(url,data=data).text
    obj = json.loads(r)
    code = obj['result']

    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('imgverifycode').clear()
    driver.find_element_by_id('imgverifycode').send_keys(code)
    driver.find_element_by_css_selector('#form > div.login_box_row.login_box_button > input.btn-submit').send_keys(Keys.ENTER)
    time.sleep(0.6)
    content = etree.HTML(driver.page_source)
    title = content.xpath('//title/text()')[0]
    # print(title)
    if title == '欢迎页 - 统一结算平台':
        cookie = json.dumps(driver.get_cookies())
        cookie_dict = json.loads(cookie)
        cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
        cookies = '; '.join(item for item in cookie_list)
        jyxy_url = 'https://fin.ane56.com/account/api/detailQuery/getBusiQuery?type=0'
        users_url = 'http://fin.ane56.com/uap/api/authorize/getUsers'
        accountinfo_url = 'https://fin.ane56.com/account/api/financeAccountMgr/getAccountInfo'
        mjy_url = 'https://fin.ane56.com/account/api/busiDetailSum/queryBusiDetailByMonth'
        aut_url = 'https://fin.ane56.com/account/api/access/auth'
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
        #网点基本信息
        site_info = json.loads(requests.post(aut_url,headers=headers).text)
        item['site_name'] = site_info['data']['siteName']
        item['site_id'] = site_info['data']['siteId']
        item['site_type'] = site_info['data']['siteVO']['siteTypeName']
        #网点用户授权
        user_data = {
         "code":"",
         "name":"",
         "userRole":"",
         "status":"N",
         "page":"1",
         "pageSize":"50",
         "deptid":item['site_id'],
        }
        getUsers_info = json.loads(requests.post(users_url,data=user_data,headers=headers).text)
        item['getUser'] = getUsers_info
        # 年经营情况
        # print('网点年经营情况:')
        jr_qk = json.loads(requests.post(mjy_url, data=data, headers=headers).text)
        item['BusiDetailByMonth'] = jr_qk['data']

        # 交易费用汇总(昨日)
        # print('交易费用汇总:')
        jy_fyhz = json.loads(requests.post(jyxy_url, headers=headers).text)
        item['yesterdayBusiQuery'] = jy_fyhz['data']
        #交易费用汇总(本月截止昨日)
        jy_fyhzyj = json.loads(requests.post(jyhzy_url,headers=headers).text)
        item['ThismonthendsyesterdayBusiQuery'] = jy_fyhzyj['data']
        # 网点当前余额
        # print('网点当前余额:')
        accountinfo = json.loads(requests.post(accountinfo_url, headers=headers).text)
        item['AccountInfo'] = accountinfo
        item['code'] = '200'
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        suc_msg = {
        "msg":"",
        "code":0,
         }
        driver.quit()
        return item
    else:
        error_msg = {
            "msg":"",
            "code":600,
        }
        driver.quit()
        print('用户授权失败')
        return error_msg






