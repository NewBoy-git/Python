from flask import Flask,jsonify,request
import pymysql
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta


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

def ymddpart():
    r = requests.get(type_url).text
    obj = json.loads(r)
    # print(obj)
    co_item = {}
    if obj["success"] == True:
        data_list = obj["data"]
        co_item["code"] = 0
        co_item["error"] = None
        co_item['msg'] = ""
        part_data = {}
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

def ymdd_login(username,password,com):
        r = requests.get(type_url).text
        obj = json.loads(r)
        data_list = obj['data']
        co_item = {}
        for data in data_list:
            co_item[data['shortName']] = data['compCode']
        #print(co_item)
        #print(com)
        #print(co_item[com])
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
        if login_status['success'] == False:
            err_msg = {'msg': '', 'code': 600}
            print(login_status)
            return err_msg
        cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
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
        this_date = datetime.datetime.now().strftime('%Y-%m-%d')
        d_m = this_date[-4]
        jy_list = []
        item_listall = {}
        for m in range(0, int(d_m) + 1):
            item = {}
            # 网点经营情况('收入月趋势')
            datetime_now = datetime.datetime.now()
            datetime_month_ago = datetime_now - relativedelta(months=int(d_m) - m)
            mon = str(datetime_month_ago)[:7]
            mon_sr = '{}月网点的收入月趋势:'.format(mon)
            srr = json.loads(
                requests.get(goods_url.format(mon, cookies['DeptCode']), headers=headers, cookies=cookies).text)

            srr['data']['mjy'] = mon_sr
            # print(srr)
            # 网点经营情况('货量月趋势')
            # print('{}月网点的货量月趋势:'.format(mon))
            mon_hl = '{}月网点的货量月趋势:'.format(mon)
            hwl = json.loads(
                requests.get(sr_url.format(mon, cookies['DeptCode']), headers=headers, cookies=cookies).text)
            hwl['data']['mhl'] = mon_hl
            # print(hwl)
            item_list = [srr['data'], hwl['data']]
            item['mon_jy'] = item_list
            # print(item)
            jy_list.append(item)
        # print(jy_list)
        item_listall['volumnAndIncomeSumPerDay'] = jy_list
        site_Pyload = {
            'dept_code': cookies['DeptCode'],
        }
        # 网点账务情况
        zwq_r = json.loads(requests.post(zw_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies).text)
        item_listall['stlAccState'] = zwq_r
        # 近30日客户货量TOP10（kg）近30日城市货量流向TOP10
        lkh = json.loads(requests.post(lkh_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies).text)
        item_listall['biDeptCharWeightInfo'] = lkh['data']
        # 网点的货物
        hw_qk = json.loads(requests.post(hw_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies).text)
        item_listall['biProjectMygoodsInfo'] = hw_qk['data']
        # 网点近30日货源
        hy_qk = json.loads(requests.post(hy_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies).text)
        item_listall['biDeptCharInterWeightInfo'] = hy_qk['data']

        # 网点当月负激励
        dy_fjl = json.loads(requests.post(fjl_url, data=json.dumps(site_Pyload), headers=headers, cookies=cookies).text)
        site_name = dy_fjl['data']['dept_name']
        item_listall['site_name'] = site_name
        item_listall['biDeptQualityControlInfo'] = dy_fjl['data']
        item_listall['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item_listall['code'] = 200
        #print(item_listall)
        return item_listall
