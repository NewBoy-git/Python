from lxml import etree

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
import warnings

warnings.filterwarnings('ignore')
import time

def baishi_spider(username,password):
    url = 'https://v5.800best.com/login'
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(r'/home/xihonglin/Flask/SiteCrawlApi/chromedriver-1', options=opt)
    driver.get(url)
    # print(driver.page_source)
    #time.sleep(0.6)

    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(0.3)
    comimg = driver.find_element_by_css_selector(
        '#app > div > div > div.g-container > div.login-container > div.login-box > div.bd > div > form > div.ant-row.ant-form-item.kaptcha > div > div > span > span > img')
    comimg.screenshot('testcode_baishi.png')
    # try:
    # 	im = Image.open('code_baishi.png')
    # 	im.show()
    # 	im.close()
    # except:
    # 	pass
    # code = input('请输入验证码:')
    import binascii

    url = 'http://api2.sz789.net:88/RecvByte.ashx'

    f = open('testcode_baishi.png', 'rb')
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
    content = etree.HTML(driver.page_source)
    dic = content.xpath(r"//pre//text()")[0]
    print(dic)
    if json.loads(dic)["code"] == "200":
        cookie_dict = json.dumps(driver.get_cookies())
        # print(cookie_dict)
        cookie_dict = json.loads(cookie_dict)
        # cookies = requests.utils.dict_from_cookiejar(cookie_dict)
        # print(cookie_dict)
        cookie = [item["name"] + "=" + item["value"] for item in cookie_dict]
        cookiestr = '; '.join(item for item in cookie)
        print(cookiestr)

        baseinfo_url = 'https://v5.800best.com/ltlv5-war/web/site/changeSite'
        Accumulation_url = 'https://v5.800best.com/ltlv5-war/web/cargoQuantity/searchCargoQuantityMonthlyTrend'
        sitemoney_url = 'https://v5.800best.com/ltlv5-war/web/balanceDetail/selectBalanceStatementBySoForFrontPage'
        ts_url = 'https://v5.800best.com/ltlv5-war/web/complaintNew/getOrderSummaryBySiteId'
        site_ys = 'https://v5.800best.com/ltlv5-war/web/cargoQuantity/searchMonthlyAccumulationTransferFee'
        recharge_url = 'https://v5.800best.com/ltlv5-war/web/aliPay/searchAlipayVo'
        users_url = 'https://v5.800best.com/ltlv5-war/web/userManage/searchPagedUserList'
        yfkRecharge_url = 'https://v5.800best.com/ltlv5-war/web/balanceDetail/searchBalanceDetail'
        yfkkz_url = 'https://v5.800best.com/ltlv5-war/web/company/searchCompany'
        #data = {
        #    'siteId': '7641851',
        #}

        headers = {
            'Accept': 'application/json, text/javascript',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '14',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookiestr,
            'Host': 'v5.800best.com',
            'Origin': 'https://v5.800best.com',
            'Referer': 'https://v5.800best.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Menu-Name': '%E9%A6%96%E9%A1%B5',
            'X-Requested-With': 'XMLHttpRequest',
        }

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
        item = {}

        # 货量月趋势
        import datetime
        import calendar as cal

        FORMAT = "%d-%d-%d"
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = []
        for m in range(1, month + 1):
            d = cal.monthrange(year, m)
            date_list1.append(FORMAT % (year, m, 1) + " 00:00:00")
        date_list3 = []
        for n in range(month-1, 13):
            d = cal.monthrange(year - 1, n)
            date_list3.append(FORMAT % (year - 1, n, 1) + " 00:00:00")

        date_list = date_list1 + date_list3

        Trend_list = []
        for _date in date_list:
            pyload = {
                "chartType": "monthTrend",
                "collectDate": _date,
            }
            month_Accumulation = json.loads(requests.post(Accumulation_url, data=json.dumps(pyload), headers=acc_headers).text)
            Trend_list.append(month_Accumulation['vo'])
            # print(month_Accumulation)
        item['monthAccumulation'] = Trend_list

        #网点营收增长
        transferFee_list = []
        for ys_date in date_list:
            ys_pyload = {
                "chartType": "revenueAccum",
                "collectDate": ys_date,
            }
            site_ys_r = json.loads(requests.post(site_ys,headers=acc_headers,data=json.dumps(ys_pyload)).text)
            transferFee_list.append(site_ys_r['voList'][-1])
        item['transferFee'] = transferFee_list
       
        # 网点账户金额
        ac_item = {}
        sitemoney_pyload = {

        }
        sitemoney_r = json.loads(requests.post(sitemoney_url, headers=acc_headers, data=json.dumps(sitemoney_pyload)).text)
        ac_item['balanceBefore'] = sitemoney_r['vo']['balanceBefore']
        ac_item['balanceTotal'] = sitemoney_r['vo']['balanceTotal']
        ac_item['currMoney'] = sitemoney_r['vo']['currMoney']
        item['balanceDetail'] = ac_item
        item['code'] = 200

        #网点充值记录
        #recharge_pyload = {
        #"currentPage":1,
        #"dateEnd":"{}-{}-1 23:59:59".format(year,month),
        #"dateStart":"{}-{}-1 00:00:00".format(year-1,month),
        #"res":"SUCCESS",
        #"pageSize":99999,
        #}
        #recharge_r = requests.post(recharge_url,data = json.dumps(recharge_pyload),headers=acc_headers).text
        #recharge_obj = json.loads(recharge_r)
        #item['autoRecharge'] = recharge_obj['pageList']
        #用户列表、
        users_pyload = {
        'currentPage':'1',
        'pageSize':'30',
        }
        user_list = json.loads(requests.post(users_url,data=json.dumps(users_pyload),headers=acc_headers).text)
        #item['userList'] = user_list['pageList']['list']
        #预付款开账
        kz_pyload = {
        'belongId':user_list['pageList']['list'][0]['companyId'],
        'currentPage':1,
        'codes':[],
        'currentPage':1,
        'depositIsShow':'true',
        'exportFull':'false',
        'name':'',
        'pageSize':'99999',
        'sorts':[],
        }
        yfkkz = json.loads(requests.post(yfkkz_url,data=json.dumps(kz_pyload),headers=acc_headers).text)
        item['userList'] = yfkkz['pageList']['list']
        #预付款充值
        yfkrecharge_pyload = {
        'bestTab':'true',
        'companyId':user_list['pageList']['list'][0]['companyId'],
        'currentPage':1,
        'dateEnd':"2019-7-1 23:59:59",
        'dateStart':"2018-7-1 00:00:00",
        'exportFull':'false',
        'pageSize':'99999',
        'priceTypeId':122,
        'priceTypeIds':[122],
        'productId':'',
        'productName':'',
        'sorts':[],
        }
        yfkRecharge = json.loads(requests.post(yfkRecharge_url,data=json.dumps(yfkrecharge_pyload),headers=acc_headers).text)
        item['yfkRecharge']=yfkRecharge['pageList']['list']
        driver.quit()
        return item
    else:
        msg = {
            "msg":"",
            "code":600
        }
        driver.quit()
        return msg
