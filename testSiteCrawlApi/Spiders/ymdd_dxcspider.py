import threading

from flask import Flask,jsonify,request
import pymysql
import requests
import json
import datetime
import calendar as cal

# from dateutil.relativedelta import relativedelta


type_url = 'https://yh.yimidida.com/galaxy-base-business/api/company/findCompany?compCode=yimidida'

url = 'https://yh.yimidida.com/galaxy-sso-business/login'

check_url = 'https://yh.yimidida.com/galaxy-user-business/sys/user/checkLoginFalseTimes?compCode=shandong&workNum=900251'

sr_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptManage/volumnAndIncomeSumPerDay.do?type=2&month={}&dept_code={}'

goods_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptManage/volumnAndIncomeSumPerDay.do?type=1&month={}&dept_code={}'

lkh_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptUpgradeKanban/outPut/biDeptCharWeightInfo.do'

zw_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptUpgradeKanban/outPut/stlAccStateMyFeeInfo.do'

hw_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptUpgradeKanban/outPut/biProjectMygoodsInfo.do'

hy_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptUpgradeKanban/outPut/biDeptCharInterWeightInfo.do'

fjl_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptUpgradeKanban/outPut/biDeptQualityControlInfo.do'

monthwigth_url = 'https://yh.yimidida.com/galaxy-bdi-business/deptManage/volumnAndIncomeSumPerMonth.do?type=1&month={}&dept_code={}'

deptinfo_url = 'https://yh.yimidida.com/galaxy-base-ext-business/sys/dept/info/queryDeptInfo?deptTypes=0,1,2,3,4,7,8&column24=9&currentPage=1&deptCode={}'

year = datetime.datetime.now().year
month = datetime.datetime.now().month
date_list1 = []
for m in range(1, month):
    if len(str(m)) < 2:
        FORMAT = "%d-0%d"
        date_list1.append(FORMAT % (year, m))
    else:
        FORMAT = "%d-%d"
        date_list1.append(FORMAT % (year, m))
date_list3 = []
for n in range(month, 13):
    if len(str(n)) < 2:
        FORMAT = "%d-0%d"
        date_list1.append(FORMAT % (year-1, n))
    else:
        FORMAT = "%d-%d"
        date_list3.append(FORMAT % (year-1, n))
date_list = date_list1 + date_list3

def ymddpart():
    r = requests.get(type_url).text
    obj = json.loads(r)
    co_item = {}
    part_data = {}
    if obj["success"] == True:
        data_list = obj["data"]
        co_item["code"] = 0
        co_item["error"] = None
        co_item['msg'] = ""
        data_lis = []
        for data in data_list:
            data_lis.append(data['shortName'])
        part_data["districtList"] = data_lis
        co_item['data'] = part_data
        return co_item
    else:
        co_item["code"] = 1
        co_item["msg"] = ""
        co_item["error"] = None
        part_data["districtList"] = []
        co_item["data"] = part_data
        return co_item
headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Host': 'yh.yimidida.com',
            'Referer': 'https://yh.yimidida.com/galaxy-nms-www/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
            'X-Token': 'undefined',
        }
cookies_item = {}
# 定义全局item
item_listall = {}
#定义线程锁
gLock = threading.Lock()
def ymdd_login(username,password,com):
        r = requests.get(type_url).text
        obj = json.loads(r)
        data_list = obj['data']
        co_item = {}
        for data in data_list:
            co_item[data['shortName']] = data['compCode']

        Pyload = {
            'appType': 1,
            'compCode': co_item[com],
            'needVCode': 'false',
            'password': password,
            'userId': 1,
            'workNum':username,
        }

        response = requests.post(url, data=json.dumps(Pyload))
        login_status = json.loads(response.text)
        print(login_status)
        print(login_status['success']==True)

        if login_status['success'] == True:
            cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
            print(cookie_dict)
            cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
            cookies_item['cookies'] = cookies
            cookies_item['code'] = 0
        else:
             cookies_item['code'] = 1
# class A(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         this_date = datetime.datetime.now().strftime('%Y-%m-%d')
#         d_m = this_date[-4]
#         jy_list = []
#         item_listall = {}
#         for m in range(0, int(d_m) + 1):
#             item = {}
#             datetime_now = datetime.datetime.now()
#             datetime_month_ago = datetime_now - relativedelta(months=int(d_m) - m)
#             mon = str(datetime_month_ago)[:7]
#             mon_sr = '{}月网点的收入月趋势:'.format(mon)
#             srr = json.loads(
#                 requests.get(goods_url.format(mon, cookies_item['cookies']['DeptCode']), headers=headers, cookies=cookies_item['cookies']).text)
#             srr['data']['mjy'] = mon_sr
#             # print(srr)
#             # 网点经营情况('货量月趋势')
#             # print('{}月网点的货量月趋势:'.format(mon))
#             mon_hl = '{}月网点的货量月趋势:'.format(mon)
#             hwl = json.loads(
#                 requests.get(sr_url.format(mon, cookies_item['cookies']['DeptCode']), headers=headers, cookies=cookies_item['cookies']).text)
#             hwl['data']['mhl'] = mon_hl
#             # print(hwl)
#             item_list = [srr['data'], hwl['data']]
#             item['mon_jy'] = item_list
#             jy_list.append(item)
#         gLock.acquire()
#         item_listall['volumnAndIncomeSumPerDay'] = jy_list
#         gLock.release()
# 网点账务情况
# class B(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         site_Pyload = {
#             'dept_code': cookies_item['cookies']['DeptCode'],
#         }
#         zwq_r = json.loads(requests.post(zw_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies_item['cookies']).text)
#         gLock.acquire()
#         item_listall['stlAccState'] = zwq_r
#         gLock.release()
# # 近30日客户货量TOP10（kg）近30日城市货量流向TOP10
# class C(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         site_Pyload = {
#             'dept_code': cookies_item['cookies']['DeptCode'],
#         }
#         lkh = json.loads(requests.post(lkh_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies_item['cookies']).text)
#         gLock.acquire()
#         item_listall['biDeptCharWeightInfo'] = lkh['data']
#         gLock.release()
#
# # 网点的货物
# class D(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         site_Pyload = {
#             'dept_code': cookies_item['cookies']['DeptCode'],
#         }
#         hw_qk = json.loads(requests.post(hw_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies_item['cookies']).text)
#         gLock.acquire()
#         item_listall['biProjectMygoodsInfo'] = hw_qk['data']
#         gLock.release()
# # 网点近30日货源
# class E(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         site_Pyload = {
#             'dept_code': cookies_item['cookies']['DeptCode'],
#         }
#         hy_qk = json.loads(requests.post(hy_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies_item['cookies']).text)
#         gLock.acquire()
#         item_listall['code'] = 200
#         item_listall['biDeptCharInterWeightInfo'] = hy_qk['data']
#         gLock.release()
# 网点当月负激励
class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        site_Pyload = {
            'dept_code': cookies_item['cookies']['DeptCode'],
        }
        dy_fjl = json.loads(requests.post(fjl_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies_item['cookies']).text)
        site_name = dy_fjl['data']['dept_name']
        gLock.acquire()
        item_listall['site_name'] = site_name
        item_listall['biDeptQualityControlInfo'] = dy_fjl['data']
        item_listall['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item_listall['code'] = 0
        gLock.release()

#网点货量月趋势
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        wigth_list = []
        for date in date_list:
            item = {}
            monthwigth_r = json.loads(requests.get(monthwigth_url.format(date,cookies_item['cookies']['DeptCode']),headers=headers, cookies=cookies_item['cookies']).text)
            chargeableWeOrIncomeSum = monthwigth_r['data']['chargeableWeOrIncomeSum']
            item['date'] = date
            item['chargeableWeOrIncomeSum'] = chargeableWeOrIncomeSum
            wigth_list.append(item)
        gLock.acquire()
        item_listall['volumnAndIncomeSumPerMonth'] = wigth_list
        gLock.release()

#网点基础信息
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        deptinfo_r = json.loads(requests.get(deptinfo_url.format(cookies_item['cookies']['DeptCode']),headers=headers,cookies=cookies_item['cookies']).text)
        gLock.acquire()
        item_listall['deptinfo'] = deptinfo_r['data']['records'][0]
        gLock.release()


#本月货量情况
class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        item = {}
        date = "{}-{}".format(year,month)
        thismonthIncomeSum = json.loads(requests.get(monthwigth_url.format(date,cookies_item['cookies']['DeptCode']),headers=headers,cookies=cookies_item['cookies']).text)
        item['date'] = date
        item['chargeableWeOrIncomeSum'] = thismonthIncomeSum['data']['chargeableWeOrIncomeSum']
        gLock.acquire()
        item_listall['thismonthIncomeSum'] = item
        gLock.release()







def ymdd_spider(username,password,com):
    ymdd_login(username,password,com)
    if cookies_item['code'] == 0:
        t1 = A()
        t1.start()
        t2 = B()
        t2.start()
        t3 = C()
        t3.start()
        # t3 = C()
        # t3.start()
        # t4 = D()
        # t4.start()
        # t5 = E()
        # t5.start()
        t6 = F()
        t6.start()
        t1.join()
        t2.join()
        t3.join()
        # t3.join()
        # t4.join()
        # t5.join()
        t6.join()
        return item_listall
    else:
        msg = {'msg':'',
               'code':600
               }
        return msg


