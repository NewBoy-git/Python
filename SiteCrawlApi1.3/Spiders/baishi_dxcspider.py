

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import json
import threading
import datetime
import calendar as cal
from lxml import etree
import warnings
import calendar

warnings.filterwarnings('ignore')
baseinfo_url = 'https://v5.800best.com/ltlv5-war/web/site/changeSite'
Accumulation_url = 'https://v5.800best.com/ltlv5-war/web/cargoQuantity/searchCargoQuantityMonthlyTrend'
sitemoney_url = 'https://v5.800best.com/ltlv5-war/web/balanceDetail/selectBalanceStatementBySoForFrontPage'
site_ys = 'https://v5.800best.com/ltlv5-war/web/cargoQuantity/searchMonthlyAccumulationTransferFee'
recharge_url = 'https://v5.800best.com/ltlv5-war/web/aliPay/searchAlipayVo'
users_url = 'https://v5.800best.com/ltlv5-war/web/userManage/searchPagedUserList'
yfkRecharge_url = 'https://v5.800best.com/ltlv5-war/web/balanceDetail/searchBalanceDetail'
yfkkz_url = 'https://v5.800best.com/ltlv5-war/web/company/searchCompany'
yfkdz_url = 'https://v5.800best.com/ltlv5-war/web/balanceDetail/selectBalanceStatementBySo'
sitesWithDistrict_url = 'https://v5.800best.com/ltlv5-war/web/site/sitesWithDistrict'

FORMAT = "%d-%d-%d"
year = datetime.datetime.now().year
month = datetime.datetime.now().month
date_list1 = []
for m in range(1, month):
    d = cal.monthrange(year, m)
    date_list1.append(FORMAT % (year, m, 1) + " 00:00:00")
date_list3 = []
for n in range(month, 13):
    d = cal.monthrange(year - 1, n)
    date_list3.append(FORMAT % (year - 1, n, 1) + " 00:00:00")
date_list = sorted(date_list1 + date_list3,reverse=True)
headers_item = {}


# 登录获取cookies
def baishi(username, password):
    url = 'https://v5.800best.com/login'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=chrome_options)
    driver.get(url)
    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(0.6)
    try:
        comimg = driver.find_element_by_css_selector(
            '#app > div > div > div.g-container > div.login-container > div.login-box > div.bd > div > form > div.ant-row.ant-form-item.kaptcha > div > div > span > span > img')
        comimg.screenshot('/home/xihonglin/Flask/SiteCrawlApi1.0/Spiders/capth_code/code_baishi.png')
        import binascii
        url = 'http://api2.sz789.net:88/RecvByte.ashx'
        f = open('/home/xihonglin/Flask/SiteCrawlApi1.0/Spiders/capth_code/code_baishi.png', 'rb')
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
        driver.find_element_by_css_selector(
            '#app > div > div > div.g-container > div.login-container > div.login-box > div.bd > div > form > div.ant-row.ant-form-item.kaptcha > div > div > span > input').clear()
        driver.find_element_by_css_selector(
            '#app > div > div > div.g-container > div.login-container > div.login-box > div.bd > div > form > div.ant-row.ant-form-item.kaptcha > div > div > span > input').send_keys(
            code)
        time.sleep(0.3)
        driver.find_element_by_css_selector(
            '#app > div > div > div.g-container > div.login-container > div.login-box > div.bd > div > form > div:nth-child(4) > div > div > button').send_keys(
            Keys.ENTER)
        time.sleep(0.3)
        driver.get('https://v5.800best.com/ltlv5-war/web/complaints/getComplaintsSummaryBySite?_=')
        time.sleep(0.3)
        print(driver.page_source)
        content = etree.HTML(driver.page_source)
        dic = content.xpath(r"//pre//text()")[0]
    except Exception as e:
        print(e)
        driver.quit()
        msg = {'code': 600,
               'msg': ''
               }
        return msg

    if json.loads(dic)["code"] == "200":
        time1 = datetime.datetime.now()
        print("登录成功", time1)
        cookie_dict = json.dumps(driver.get_cookies())
        print(cookie_dict)
        cookie_dict = json.loads(cookie_dict)
        cookie = [item["name"] + "=" + item["value"] for item in cookie_dict]
        cookiestr = '; '.join(item for item in cookie)
        acc_headers = {
            'Accept': 'application/json, text/javascript',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '62',
            'Content-Type': 'application/json',
            'Cookie': cookiestr,
            'Host': 'v5.800best.com',
            'Origin': 'https://v5.800best.com',
            'Referer': 'https://v5.800best.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Menu-Name': '%E9%A6%96%E9%A1%B5',
            'X-Requested-With': 'XMLHttpRequest',
        }
        headers_item['code'] = 0
        headers_item['acc_headers'] = acc_headers
    else:
        headers_item['code'] = 1


# 定义全局item，线程锁
item = {}

gLock = threading.Lock()


# 网点营收增长
class S(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        ac_item = {}
        sitemoney_pyload = {

        }
        sitemoney_r = json.loads(
            requests.post(sitemoney_url, headers=headers_item['acc_headers'], data=json.dumps(sitemoney_pyload)).text)
        ac_item['balanceBefore'] = sitemoney_r['vo']['balanceBefore']
        ac_item['balanceTotal'] = sitemoney_r['vo']['balanceTotal']
        ac_item['currMoney'] = sitemoney_r['vo']['currMoney']
        gLock.acquire()
        item['balanceDetail'] = ac_item
        gLock.release()


# 货量月趋势
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        Trend_list = []
        for _date in date_list:
            pyload = {
                "chartType": "monthTrend",
                "collectDate": _date,
            }
            month_Accumulation = json.loads(
                requests.post(Accumulation_url, data=json.dumps(pyload), headers=headers_item['acc_headers']).text)['vo']
            month_Accumulation['date'] = _date
            Trend_list.append(month_Accumulation)
        gLock.acquire()
        item['monthAccumulation'] = Trend_list
        gLock.release()

# 预付款开账
class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)
        gLock.acquire()
        item['userList'] = user_list['pageList']['list']
        item['code'] = 200
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gLock.release()


monthRange = calendar.monthrange(year, month - 1)
monthRange = monthRange[1]


# 预付款对账统计---一级,二级网点奖罚,一级网点派件费，一二级总体充值费

class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = sorted(date_list1 + date_list3, reverse=True)
        
        firAndSecStatementBySo_list = []
        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)
        for date in ywdateend_list:
            firAndSec_pyload = {
                'bestTab': 'true',
                'currentPage': 1,
                'dateEnd': "{}-{}-{} 23:59:59".format(date[0], date[1], date[2]),
                'dateStart': "{}-{}-1 00:00:00".format(date[0], date[1]),
                'franchiseeId': user_list['pageList']['list'][0]['companyId'],
                'pageSize': '99999',
            }
            StatementBySo = json.loads(
                requests.post(yfkdz_url, data=json.dumps(firAndSec_pyload), headers=headers_item['acc_headers']).text)['pageList']['list'][0]
            if len(str(date[1]))<2:
                StatementBySo['date'] = "{}-0{}".format(date[0],date[1])
            else:
                StatementBySo['date'] = "{}-{}".format(date[0],date[1])
            firAndSecStatementBySo_list.append(StatementBySo)

        gLock.acquire()
        item['firAndSecStatementBySo'] =  firAndSecStatementBySo_list
        gLock.release()


# 预付款对账统计---一级及下属网点

class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = sorted(date_list1 + date_list3, reverse=True)
        
        allStatementBySo_list = []
        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)
        for date in ywdateend_list:
            all_pyload = {
                'bestTab': 'false',
                'currentPage': '1',
                'dateEnd': "{}-{}-{} 23:59:59".format(date[0],date[1],date[2]),
                'dateStart': "{}-{}-1 00:00:00".format(date[0],date[1]),
                'franchiseeId': 'null',
                'pageSize': '99999',
                'settleId': user_list['pageList']['list'][0]['companyId'],
            }
            StatementBySo = json.loads(
                requests.post(yfkdz_url, data=json.dumps(all_pyload), headers=headers_item['acc_headers']).text)['pageList']
            if len(str(date[1]))<2:
                StatementBySo['date'] = "{}-0{}".format(date[0],date[1])
            else:
                StatementBySo['date'] = "{}-{}".format(date[0],date[1])
            allStatementBySo_list.append(StatementBySo)
        gLock.acquire()
        item['allStatementBySo'] = allStatementBySo_list
        item['code'] = 200
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gLock.release()


# 网点状态信息
class G(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)

        status_pyload = {
            'pageSize': 30,
            'currentPage': 1,
            'pageNumber': 1,
            'status': 'null',
            'statuses': ["ENABLE"],
            'name': user_list['pageList']['list'][0]["ownerSiteName"]
        }
        siteStatus_r = json.loads(requests.post(sitesWithDistrict_url, data=json.dumps(status_pyload),
                                                headers=headers_item['acc_headers']).text)
        gLock.acquire()
        item['siteName'] = user_list['pageList']['list'][0]["ownerSiteName"]
        item['siteStatus'] = siteStatus_r['pageList']['list']
        gLock.release()

#本月截止当日
class H(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        date = str(datetime.datetime.now())

        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)

        all_pyload = {
                'bestTab': 'false',
                'currentPage': '1',
                'dateEnd': "{}-{}-{} 00:00:00".format(date[0:4], date[5:7], date[8:10]),
                'dateStart': "{}-{}-1 00:00:00".format(date[0:4], date[5:7]),
                'franchiseeId': 'null',
                'pageSize': '99999',
                'settleId': user_list['pageList']['list'][0]['companyId'],
            }
        StatementBySo = json.loads(
                requests.post(yfkdz_url, data=json.dumps(all_pyload), headers=headers_item['acc_headers']).text)[
                'pageList']['list']
        gLock.acquire()
        item['thismonthallStatementBySo'] = StatementBySo
        gLock.release()

class I(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        date = str(datetime.datetime.now())

        users_pyload = {
            'currentPage': '1',
            'pageSize': '30',
        }
        user_list = json.loads(
            requests.post(users_url, data=json.dumps(users_pyload), headers=headers_item['acc_headers']).text)

        firAndSec_pyload = {
                'bestTab': 'true',
                'currentPage': 1,
                'dateEnd': "{}-{}-{} 00:00:00".format(date[0:4], date[5:7], date[8:10]),
                'dateStart': "{}-{}-1 00:00:00".format(date[0:4], date[5:7]),
                'franchiseeId': user_list['pageList']['list'][0]['companyId'],
                'pageSize': '99999',
            }
        StatementBySo = json.loads(
                requests.post(yfkdz_url, data=json.dumps(firAndSec_pyload), headers=headers_item['acc_headers']).text)[
                'pageList']['list'][0]
        gLock.acquire()
        item['thismonthfirAndSecStatementBySo'] = StatementBySo
        item['siteCode'] = StatementBySo['franchiseeCode']
        gLock.release()


def baishi_spider(username, password):
    baishi(username, password)
    if headers_item['code'] == 0:
        t1 = A()
        t1.start()
        t2 = E()
        t2.start()
        t3 = F()
        t3.start()
        t4 = S()
        t4.start()
        t5 = D()
        t5.start()
        t6 = G()
        t6.start()
        t7 = H()
        t7.start()
        t8 = I()
        t8.start()


        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        return item
    else:
        msg = {'code': 600,
               'msg': ''
               }
        return msg


