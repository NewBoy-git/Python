import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import datetime
import calendar
import binascii
import requests
from lxml import etree

import threading
import re
#test dev

item_all = {}
ztList = []
yjztList = []
gLock = threading.Lock()

sid = int((time.time()*1000)%9999+1)
zk_url = 'http://sxne.sxjdfreight.com/zkau'

FORMAT = "%d-%d-%d"
year = datetime.datetime.now().year
month = datetime.datetime.now().month
date_list1 = [FORMAT % (year, m, calendar.monthrange(year, m)[1]) for m in range(1,month)]
date_list6 = [FORMAT % (year, m, 1) for m in range(1,month)]
date_list3 = [FORMAT % (year - 1, n, calendar.monthrange(year - 1, n)[1]) for n in range(month,13)]
date_list9 = [FORMAT % (year - 1, n, 1) for n in range(month,13)]
datesta_list = date_list6 + date_list9
dateend_list = date_list1 + date_list3




cookie_item = {}
def jd_login(username,password):
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
            cookies = json.dumps(driver.get_cookies())
            cookie_dict = json.loads(cookies)
            cookie_list = [item["name"] + "=" + item["value"] for item in cookie_dict]
            cookies_jd = '; '.join(item for item in cookie_list)
            cookie_item['site_name'] = sitename
            cookie_item['cookies_jd'] = cookies_jd
            cookie_item['code'] = 0
            with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/jdcookies.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(cookie_item))
            driver.quit()
            return cookie_item
        else:
            cookie_item['code'] =1
            with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/jdcookie.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(cookie_item))
            driver.quit()
            return cookie_item
    except Exception as e:
        driver.quit()
        print(e)
        cookie_item['code'] = 1
        with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/jdcookie.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(cookie_item))
        return cookie_item


#网点业务信息
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        yw_url = 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul'
        headers = {
            'Cookie':cookie_item['cookies_jd']
        }
        yw_res = requests.get(yw_url,headers=headers).text

        dtid_body = "id:'pg_EwbSend',dt:'(.*?)',"
        pattern_dtid = re.compile(dtid_body)
        dtid_code = re.findall(pattern_dtid,yw_res)[0]


        datesta_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtbStart',"
        pattern_sta = re.compile(datesta_body)
        datesta_code = re.findall(pattern_sta,yw_res)[0]

        dateend_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtbEnd',"
        pattern_end = re.compile(dateend_body)
        dateend_code = re.findall(pattern_end,yw_res)[0]

        search_body = "'zul.wgt.Button','(.*?)',{id:'btnSearch',"
        pattern_search = re.compile(search_body)
        search_code = re.findall(pattern_search,yw_res)[0]

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = date_list1 + date_list3
        print(ywdateend_list)

        ps_body = "'zul.wgt.Label','(.*?)',{id:'lblVotes',"
        js_body = "'zul.wgt.Label','(.*?)',{id:'lblPiece',"
        jswidth_body = "'zul.wgt.Label','(.*?)',{id:'lblCalcWeight',"
        zzjswidth_body = "'zul.wgt.Label','(.*?)',{id:'lblTransferCalcWeight',"
        sjwidth_body = "'zul.wgt.Label','(.*?)',{id:'lblAcWeight',"
        tj_body = "'zul.wgt.Label','(.*?)',{id:'lblVol',"
        dfk_body = "'zul.wgt.Label','(.*?)',{id:'lblArriveAmount',"
        xj_body = "'zul.wgt.Label','(.*?)',{id:'lblCash',"
        yj_body = "'zul.wgt.Label','(.*?)',{id:'lblMonth',"
        yfhj_body = "'zul.wgt.Label','(.*?)',{id:'lblFreightSum',"
        sfhj_body = "'zul.wgt.Label','(.*?)',{id:'lblChargeInTotal',"
        cbhj_body = "'zul.wgt.Label','(.*?)',{id:'lblCostTotal',"
        ml_body = "'zul.wgt.Label','(.*?)',{id:'lblGrossMargin',"

        pattern_ps = re.compile(ps_body)
        pattern_js = re.compile(js_body)
        pattern_jswidth = re.compile(jswidth_body)
        pattern_zzjswidth = re.compile(zzjswidth_body)
        pattern_sjwidth = re.compile(sjwidth_body)
        pattern_tj = re.compile(tj_body)
        pattern_dfk = re.compile(dfk_body)
        pattern_xj = re.compile(xj_body)
        pattern_yj = re.compile(yj_body)
        pattern_yfhj = re.compile(yfhj_body)
        pattern_sfhj = re.compile(sfhj_body)
        pattern_cbhj = re.compile(cbhj_body)
        pattern_ml = re.compile(ml_body)

        ps_code = re.findall(pattern_ps,yw_res)[0]
        js_code = re.findall(pattern_js,yw_res)[0]
        jswidth_code = re.findall(pattern_jswidth,yw_res)[0]
        zzjswidth_code = re.findall(pattern_zzjswidth,yw_res)[0]
        sjwidth_code = re.findall(pattern_sjwidth,yw_res)[0]
        tj_code = re.findall(pattern_tj,yw_res)[0]
        dfk_code = re.findall(pattern_dfk,yw_res)[0]
        xj_code = re.findall(pattern_xj,yw_res)[0]
        yj_code = re.findall(pattern_yj,yw_res)[0]
        yfhj_code = re.findall(pattern_yfhj,yw_res)[0]
        sfhj_code = re.findall(pattern_sfhj,yw_res)[0]
        cbhj_code = re.findall(pattern_cbhj,yw_res)[0]
        ml_code = re.findall(pattern_ml,yw_res)[0]
        print('ywlist****************************')
        yw_list = []
        for date in ywdateend_list:
            item = {}
            item['date'] = "{}-{}".format(date[0],date[1])
            yw_data = {
                'dtid': dtid_code,
                'cmd_0': 'onChange',
                'uuid_0': datesta_code,
                'data_0': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.1.0.0.0.0","start":10}',
                'cmd_1': 'onChange',
                'uuid_1': dateend_code,
                'data_1': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                            date[2]) + '.23.59.59.0","start":10}',
                'cmd_2': 'onClick',
                'uuid_2': search_code,
                'data_2': '{"pageX":56,"pageY":18,"which":1,"x":49,"y":16}',
            }

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '360',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Cookie': cookie_item['cookies_jd'],
                'Host': 'sxne.sxjdfreight.com',
                'Origin': 'http://sxne.sxjdfreight.com',
                'Referer': 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'ZK-SID': str(sid),
            }
            sid+=1
            print(sid)
            yw_info = requests.post(zk_url,data=yw_data,headers=headers).text
            # print(yw_info)
            # value_body = '"value","(.*?)"'
            # value_pattern = re.compile(value_body)
            # vaule_list = re.findall(value_pattern, yw_info)
            # print(vaule_list)
            ps_body = '{\\$u:'+"'"+ps_code+"'"+r'},"value","(.*?)"'
            ps_pattern = re.compile(str(ps_body))
            ps_list = re.findall(ps_pattern,yw_info)
            if ps_list != []:
                item['ps_'] = ps_list[0]
            else:
                item['ps_'] = '0.00'

            js_body = '{\\$u:' + "'" + js_code + "'" + r'},"value","(.*?)"'
            js_pattern = re.compile(str(js_body))
            js_list = re.findall(js_pattern, yw_info)
            if js_list != []:
                item['js_'] = js_list[0]
            else:
                item['js_'] = '0.00'

            jswidth_body = '{\\$u:' + "'" + jswidth_code + "'" + r'},"value","(.*?)"'
            jswidth_pattern = re.compile(str(jswidth_body))
            jswidth_list = re.findall(jswidth_pattern , yw_info)
            if jswidth_list != []:
                item['jswidth'] = jswidth_list[0]
            else:
                item['jswidth'] = '0.00'

            zzjswidth_body = '{\\$u:' + "'" + zzjswidth_code + "'" + r'},"value","(.*?)"'
            zzjswidth_pattern = re.compile(str(zzjswidth_body))
            zzjswidth_list = re.findall(zzjswidth_pattern, yw_info)
            if zzjswidth_list != []:
                item['zzjswidth'] = zzjswidth_list[0]
            else:
                item['zzjswidth'] = '0.00'

            sjwidth_body = '{\\$u:' + "'" + sjwidth_code + "'" + r'},"value","(.*?)"'
            sjwidth_pattern = re.compile(str(sjwidth_body))
            sjwidth_list = re.findall(sjwidth_pattern, yw_info)
            if sjwidth_list != []:
                item['sjwidth'] = sjwidth_list[0]
            else:
                item['sjwidth'] = '0.00'

            tj_body  = '{\\$u:' + "'" + tj_code + "'" + r'},"value","(.*?)"'
            tj_pattern = re.compile(str(tj_body))
            tj_list = re.findall(tj_pattern, yw_info)
            if tj_list != []:
                item['tj_'] = tj_list[0]
            else:
                item['tj_'] = '0.00'

            dfk_body = '{\\$u:' + "'" + dfk_code + "'" + r'},"value","(.*?)"'
            dfk_pattern = re.compile(str(dfk_body))
            dfk_list = re.findall(dfk_pattern,yw_info)
            if dfk_list != []:
                item['dfk'] = dfk_list[0]
            else:
                item['dfk'] = '0.00'

            xj_body = '{\\$u:' + "'" + xj_code + "'" + r'},"value","(.*?)"'
            xj_pattern = re.compile(str(xj_body))
            xj_list = re.findall(xj_pattern,yw_info)
            if xj_list != []:
                item['xj_'] = xj_list[0]
            else:
                item['xj_'] = '0.00'

            yj_body = '{\\$u:' + "'" + yj_code + "'" + r'},"value","(.*?)"'
            yj_pattern = re.compile(str(yj_body))
            yj_list = re.findall(yj_pattern,yw_info)
            if yj_list != []:
                item['yj_'] = yj_list[0]
            else:
                item['yj_'] = '0.00'




            yfhj_body = '{\\$u:' + "'" + yfhj_code + "'" + r'},"value","(.*?)"'
            yfhj_pattern = re.compile(str(yfhj_body))
            yfhj_list = re.findall(yfhj_pattern,yw_info)
            if yfhj_list != []:
                item['yfhj'] = yfhj_list[0]
            else:
                item['yfhj'] = '0.00'

            sfhj_body = '{\\$u:' + "'" + sfhj_code + "'" + r'},"value","(.*?)"'
            sfhj_pattern = re.compile(str(sfhj_body))
            sfhj_list = re.findall(sfhj_pattern,yw_info)
            if sfhj_list != []:
                item['sfhj'] = sfhj_list[0]
            else:
                item['sfhj'] = '0.00'


            cbhj_body = '{\\$u:' + "'" + cbhj_code + "'" + r'},"value","(.*?)"'
            cbhj_pattern = re.compile(str(cbhj_body))
            cbhj_list = re.findall(cbhj_pattern,yw_info)
            if cbhj_list != []:
                item['cbhj'] = cbhj_list[0]
            else:
                item['cbhj'] = '0.00'

            ml_body = '{\\$u:' + "'" + ml_code + "'" + r'},"value","(.*?)"'
            ml_pattern = re.compile(str(ml_body))
            ml_list = re.findall(ml_pattern,yw_info)
            if ml_list != []:
                item['ml_'] = ml_list[0]
            else:
                item['ml_'] = '0.00'
            yw_list.append(item)
        gLock.acquire()
        item_all['ztList'] = yw_list
        gLock.release()

#网点业务信息，1级
class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        yw_url = 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul'
        headers = {
            'Cookie':cookie_item['cookies_jd']
        }
        yw_res = requests.get(yw_url, headers=headers).text
        # print(yw_res)
        dtid_body = "id:'pg_EwbSend',dt:'(.*?)',"
        pattern_dtid = re.compile(dtid_body)
        dtid_code = re.findall(pattern_dtid, yw_res)[0]

        datesta_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtbStart',"
        pattern_sta = re.compile(datesta_body)
        datesta_code = re.findall(pattern_sta, yw_res)[0]

        dateend_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtbEnd',"
        pattern_end = re.compile(dateend_body)
        dateend_code = re.findall(pattern_end, yw_res)[0]

        search_body = "'zul.wgt.Button','(.*?)',{id:'btnSearch',"
        pattern_search = re.compile(search_body)
        search_code = re.findall(pattern_search, yw_res)[0]

        sendsite_body = "'zul.inp.Textbox','(.*?)',{id:'txtSendSite',"
        pattern_sendsite = re.compile(sendsite_body)
        sendsite_code = re.findall(pattern_sendsite, yw_res)[0]

        sitename = cookie_item['site_name']
        sendsite_data = {
            'dtid': dtid_code,
            'cmd_0': 'onChanging',
            'opt_0': 'i',
            'uuid_0': sendsite_code,
            'data_0': '{"value":'+'"'+sitename+'"'+',"start":'+str(len(sitename))+'}',
        }

        sendsite_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '185',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie':cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid),
        }

        sendsite_r = requests.post(zk_url, data=sendsite_data, headers=sendsite_headers).text
        # print(sendsite_r)

        sendsiteclick_data = {
            'dtid': dtid_code,
            'cmd_0': 'onChange',
            'uuid_0': sendsite_code,
            'data_0': '{"value":'+'"'+sitename+'"'+',"start":'+str(len(sitename))+'}',
            'cmd_1': 'onBlur',
            'uuid_1': sendsite_code,
        }

        sendsiteclick_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '202',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie':cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1),
        }

        sendsiteclick_r = requests.post(zk_url, data=sendsiteclick_data, headers=sendsiteclick_headers).text
        print(sendsiteclick_data)

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = date_list1 + date_list3
        print(ywdateend_list)

        ps_body = "'zul.wgt.Label','(.*?)',{id:'lblVotes',"
        js_body = "'zul.wgt.Label','(.*?)',{id:'lblPiece',"
        jswidth_body = "'zul.wgt.Label','(.*?)',{id:'lblCalcWeight',"
        zzjswidth_body = "'zul.wgt.Label','(.*?)',{id:'lblTransferCalcWeight',"
        sjwidth_body = "'zul.wgt.Label','(.*?)',{id:'lblAcWeight',"
        tj_body = "'zul.wgt.Label','(.*?)',{id:'lblVol',"
        dfk_body = "'zul.wgt.Label','(.*?)',{id:'lblArriveAmount',"
        xj_body = "'zul.wgt.Label','(.*?)',{id:'lblCash',"
        yj_body = "'zul.wgt.Label','(.*?)',{id:'lblMonth',"
        yfhj_body = "'zul.wgt.Label','(.*?)',{id:'lblFreightSum',"
        sfhj_body = "'zul.wgt.Label','(.*?)',{id:'lblChargeInTotal',"
        cbhj_body = "'zul.wgt.Label','(.*?)',{id:'lblCostTotal',"
        ml_body = "'zul.wgt.Label','(.*?)',{id:'lblGrossMargin',"

        pattern_ps = re.compile(ps_body)
        pattern_js = re.compile(js_body)
        pattern_jswidth = re.compile(jswidth_body)
        pattern_zzjswidth = re.compile(zzjswidth_body)
        pattern_sjwidth = re.compile(sjwidth_body)
        pattern_tj = re.compile(tj_body)
        pattern_dfk = re.compile(dfk_body)
        pattern_xj = re.compile(xj_body)
        pattern_yj = re.compile(yj_body)
        pattern_yfhj = re.compile(yfhj_body)
        pattern_sfhj = re.compile(sfhj_body)
        pattern_cbhj = re.compile(cbhj_body)
        pattern_ml = re.compile(ml_body)

        ps_code = re.findall(pattern_ps, yw_res)[0]
        js_code = re.findall(pattern_js, yw_res)[0]
        jswidth_code = re.findall(pattern_jswidth, yw_res)[0]
        zzjswidth_code = re.findall(pattern_zzjswidth, yw_res)[0]
        sjwidth_code = re.findall(pattern_zzjswidth, yw_res)[0]
        tj_code = re.findall(pattern_tj, yw_res)[0]
        dfk_code = re.findall(pattern_dfk, yw_res)[0]
        xj_code = re.findall(pattern_xj, yw_res)[0]
        yj_code = re.findall(pattern_yj, yw_res)[0]
        yfhj_code = re.findall(pattern_yfhj, yw_res)[0]
        sfhj_code = re.findall(pattern_sfhj, yw_res)[0]
        cbhj_code = re.findall(pattern_cbhj, yw_res)[0]
        ml_code = re.findall(pattern_ml, yw_res)[0]

        print('yjywlis****************************')

        yjyw_list = []
        for date in ywdateend_list:
            item = {}
            item['date'] = "{}-{}".format(date[0], date[1])
            yw_data = {
                'dtid': dtid_code,
                'cmd_0': 'onChange',
                'uuid_0': datesta_code,
                'data_0': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.1.0.0.0.0","start":10}',
                'cmd_1': 'onChange',
                'uuid_1': dateend_code,
                'data_1': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                    date[2]) + '.23.59.59.0","start":10}',
                'cmd_2': 'onClick',
                'uuid_2': search_code,
                'data_2': '{"pageX":56,"pageY":18,"which":1,"x":49,"y":16}',
            }

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '360',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Cookie': cookie_item['cookies_jd'],
                'Host': 'sxne.sxjdfreight.com',
                'Origin': 'http://sxne.sxjdfreight.com',
                'Referer': 'http://sxne.sxjdfreight.com/ne1/operation/ewb_send_mi_mgr3.zul',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'ZK-SID': str(sid + 1 + 1),
            }
            sid += 1
            print(sid)
            yw_info = requests.post(zk_url, data=yw_data, headers=headers).text
            # print(yw_info)
            # value_body = '"value","(.*?)"'
            # value_pattern = re.compile(value_body)
            # vaule_list = re.findall(value_pattern, yw_info)
            # print(vaule_list)
            ps_body = '{\\$u:' + "'" + ps_code + "'" + r'},"value","(.*?)"'
            ps_pattern = re.compile(str(ps_body))
            ps_list = re.findall(ps_pattern, yw_info)
            if ps_list != []:
                item['ps_'] = ps_list[0]
            else:
                item['ps_'] = '0.00'

            js_body = '{\\$u:' + "'" + js_code + "'" + r'},"value","(.*?)"'
            js_pattern = re.compile(str(js_body))
            js_list = re.findall(js_pattern, yw_info)
            if js_list != []:
                item['js_'] = js_list[0]
            else:
                item['js_'] = '0.00'

            jswidth_body = '{\\$u:' + "'" + jswidth_code + "'" + r'},"value","(.*?)"'
            jswidth_pattern = re.compile(str(jswidth_body))
            jswidth_list = re.findall(jswidth_pattern, yw_info)
            if jswidth_list != []:
                item['jswidth'] = jswidth_list[0]
            else:
                item['jswidth'] = '0.00'

            zzjswidth_body = '{\\$u:' + "'" + zzjswidth_code + "'" + r'},"value","(.*?)"'
            zzjswidth_pattern = re.compile(str(zzjswidth_body))
            zzjswidth_list = re.findall(zzjswidth_pattern, yw_info)
            if zzjswidth_list != []:
                item['zzjswidth'] = zzjswidth_list[0]
            else:
                item['zzjswidth'] = '0.00'

            sjwidth_body = '{\\$u:' + "'" + sjwidth_code + "'" + r'},"value","(.*?)"'
            sjwidth_pattern = re.compile(str(sjwidth_body))
            sjwidth_list = re.findall(sjwidth_pattern, yw_info)
            if sjwidth_list != []:
                item['sjwidth'] = sjwidth_list[0]
            else:
                item['sjwidth'] = '0.00'

            tj_body = '{\\$u:' + "'" + tj_code + "'" + r'},"value","(.*?)"'
            tj_pattern = re.compile(str(tj_body))
            tj_list = re.findall(tj_pattern, yw_info)
            if tj_list != []:
                item['tj_'] = tj_list[0]
            else:
                item['tj_'] = '0.00'

            dfk_body = '{\\$u:' + "'" + dfk_code + "'" + r'},"value","(.*?)"'
            dfk_pattern = re.compile(str(dfk_body))
            dfk_list = re.findall(dfk_pattern, yw_info)
            if dfk_list != []:
                item['dfk'] = dfk_list[0]
            else:
                item['dfk'] = '0.00'

            xj_body = '{\\$u:' + "'" + xj_code + "'" + r'},"value","(.*?)"'
            xj_pattern = re.compile(str(xj_body))
            xj_list = re.findall(dfk_pattern, yw_info)
            if xj_list != []:
                item['xj_'] = xj_list[0]
            else:
                item['xj_'] = '0.00'

            yj_body = '{\\$u:' + "'" + yj_code + "'" + r'},"value","(.*?)"'
            yj_pattern = re.compile(str(yj_body))
            yj_list = re.findall(yj_pattern, yw_info)
            if yj_list != []:
                item['yj_'] = yj_list[0]
            else:
                item['yj_'] = '0.00'

            yfhj_body = '{\\$u:' + "'" + yfhj_code + "'" + r'},"value","(.*?)"'
            yfhj_pattern = re.compile(str(yfhj_body))
            yfhj_list = re.findall(yfhj_pattern, yw_info)
            if yfhj_list != []:
                item['yfhj'] = yfhj_list[0]
            else:
                item['yfhj'] = '0.00'

            sfhj_body = '{\\$u:' + "'" + sfhj_code + "'" + r'},"value","(.*?)"'
            sfhj_pattern = re.compile(str(sfhj_body))
            sfhj_list = re.findall(sfhj_pattern, yw_info)
            if sfhj_list != []:
                item['sfhj'] = sfhj_list[0]
            else:
                item['sfhj'] = '0.00'

            cbhj_body = '{\\$u:' + "'" + cbhj_code + "'" + r'},"value","(.*?)"'
            cbhj_pattern = re.compile(str(cbhj_body))
            cbhj_list = re.findall(cbhj_pattern, yw_info)
            if cbhj_list != []:
                item['cbhj'] = cbhj_list[0]
            else:
                item['cbhj'] = '0.00'

            ml_body = '{\\$u:' + "'" + ml_code + "'" + r'},"value","(.*?)"'
            ml_pattern = re.compile(str(ml_body))
            ml_list = re.findall(ml_pattern, yw_info)
            if ml_list != []:
                item['ml_'] = ml_list[0]
            else:
                item['ml_'] = '0.00'
            yjyw_list.append(item)
            gLock.acquire()
            item_all['yjztList'] = yjyw_list
            gLock.release()



#网点名称，关联公司
class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        url = 'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul'
        headers = {
            'Cookie': cookie_item['cookies_jd'],
        }

        r = requests.get(url, headers=headers).text
        # print(r)
        body_dtid = r"id:'.*?',dt:'(.*?)'"
        pattern_dtid = re.compile(body_dtid)
        dtid = re.findall(pattern_dtid, r)[0]
        print(dtid)

        body_sta = r"'zul.db.Datebox','(.*?)',.*',id:'dtSearchStartDate',"
        pattern_sta = re.compile(body_sta)
        datesta_code = re.findall(pattern_sta, r)[0]

        body_end = r"'zul.db.Datebox','(.*?)',.*',id:'dtSearchEndDate',"
        pattern_end = re.compile(body_end)
        dateend_code = re.findall(pattern_end, r)[0]

        body_search = r"zul.wgt.Button','(.*?)',{id:'btnSearch',.*"
        pattern_search = re.compile(body_search)
        search_code = re.findall(pattern_search, r)[0]

        # print(dtid)
        # print(datesta_code)
        # print(dateend_code)
        # print(search_code)

        data_sta = {
            'dtid': dtid,
            'cmd_0': 'onChange',
            'uuid_0': datesta_code,
            'data_0': '{"value":"$z!t#d:2018.9.1.0.0.0.201","start":10}',
            'cmd_1': 'onBlur',
            'uuid_1': datesta_code
        }

        headers1 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '150',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid),
        }
        r1 = requests.post(zk_url, data=data_sta, headers=headers1)
        # print(r1.text)

        data_end = {
            'dtid': dtid,
            'cmd_0': 'onChange',
            'uuid_0': dateend_code,
            'data_0': '{"value":"$z!t#d:2019.8.31.23.59.59.201","start":10}',
            'cmd_1': 'onBlur',
            'uuid_1': dateend_code
        }

        headers2 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '150',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1),
        }
        r2 = requests.post(zk_url, data=data_end, headers=headers2)

        print(r2.text)
        data_search = {
            'dtid': dtid,
            'cmd_0': 'onClick',
            'uuid_0': search_code,
            'data_0': '{"pageX":60,"pageY":54,"which":1,"x":48,"y":16}',
        }

        headers3 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '134',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1 + 1),
        }

        r = requests.post(zk_url, data=data_search, headers=headers3).text
        r = r.replace(r'\"', '"').strip("loadGridData([])")

        body_name = '"SITE_NAME":"(.*?)"'
        pattern_name = re.compile(body_name)
        sitename = re.findall(pattern_name, r)[0]

        body_fk = r'"94":(.*?),'
        pattern_fk = re.compile(body_fk)
        fk_je = re.findall(pattern_fk, r)[0]

        body_com = r'"LEGAL_NAME":"(.*?)"'
        pattern_com = re.compile(body_com)
        com = re.findall(pattern_com, r)[0]

        print('comename*******************')

        gLock.acquire()
        item_all['siteName'] = sitename
        item_all['frCompany'] = com
        gLock.release()

#网点仲裁罚款
class D(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        headers = {
        'Cookie': cookie_item['cookies_jd'],
        }

        hzzd_r = requests.get('http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',headers=headers).text

        # print(hzzd_r)
        dtid_body = "{id:'pg_fin_bill_sum_necp',dt:'(.*?)',"
        pattern_dtid = re.compile(dtid_body)
        dtid = re.findall(pattern_dtid,hzzd_r)[0]
        # print(dtid)

        search_body = "'zul.wgt.Button','(.*?)',{id:'btnSearch',"
        pattern_search = re.compile(search_body)
        search_code = re.findall(pattern_search,hzzd_r)[0]

        startdate_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtSearchStartDate',"
        pattern_sta = re.compile(startdate_body)
        startdate_code = re.findall(pattern_sta,hzzd_r)[0]

        enddate_body = "'zul.db.Datebox','(.*?)',{format:'yyyy-MM-dd',id:'dtSearchEndDate',"
        pattern_end = re.compile(enddate_body)
        enddate_code = re.findall(pattern_end,hzzd_r)[0]
        print('zcfk************************************')

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = date_list1 + date_list3
        print(ywdateend_list)

        list = []
        for date in ywdateend_list:
            item = {}
            item['date'] = "{}-{}".format(date[0], date[1])
            datasta = {
            'dtid':dtid,
            'cmd_0':'onChange',
            'uuid_0':startdate_code,
            'data_0':'{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) +'.' +'1.0.0.0.355","start":10}',
            'cmd_1':'onBlur',
            'uuid_1':startdate_code,
            }
            print('{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) +'.' +'1.0.0.0.355","start":10}')
            datasta_headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'150',
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host':'sxne.sxjdfreight.com',
            'Origin':'http://sxne.sxjdfreight.com',
            'Referer':'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID':str(sid),
            }

            sta_r = requests.post(zk_url,data=datasta,headers=datasta_headers).text
            # print(sta_r)

            dataend = {
            'dtid':dtid,
            'cmd_0':'onChange',
            'uuid_0':enddate_code,
            'data_0':'{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                            date[2]) + '.23.59.59.355","start":10}',
            'cmd_1':'onBlur',
            'uuid_1':enddate_code,
            }

            print('{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                            date[2]) + '.23.59.59.355","start":10}')
            headersend = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'154',
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host':'sxne.sxjdfreight.com',
            'Origin':'http://sxne.sxjdfreight.com',
            'Referer':'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID':str(sid+1),
            }
            end_r = requests.post(zk_url,data=dataend,headers=headersend).text

            # print(end_r)

            data_search = {
            'dtid': dtid,
            'cmd_0':'onClick',
            'uuid_0':search_code,
            'data_0':'{"pageX":54,"pageY":48,"which":1,"x":42,"y":10}',
            }

            headersearch = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'134',
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host':'sxne.sxjdfreight.com',
            'Origin':'http://sxne.sxjdfreight.com',
            'Referer':'http://sxne.sxjdfreight.com/ne1/finance/fin_bill_sum_necp.zul',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID':str(sid+1+1)
            }

            search_r = requests.post(zk_url,data=data_search,headers=headersearch).text
            search_r = search_r.replace(r'\"','"')
            print(search_r)
            zcfk_body = ',"(\d+)-仲裁罚款",'
            pattern_zcfk = re.compile(zcfk_body)
            zc_fk = re.findall(pattern_zcfk,search_r)[0]
            # print(zc_fk)
            try:
                co_body = '"'+zc_fk+'"'+":(.*?),"
                print(co_body)
                pattern_co = re.compile(co_body)
                fk_je = re.findall(pattern_co,search_r)[0]
                if fk_je == '':
                    fk_je='0'
                else:
                    fk_je=fk_je
            except Exception as e:
                fk_je = '0'
            print(fk_je)
            item['zcfk'] = fk_je
            list.append(item)
        gLock.acquire()
        item_all['zcfkList'] = list
        gLock.release()

#网点基础信息
class E(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        headers = {
            'Cookie': cookie_item['cookies_jd'],
        }
        part_r = requests.get('http://sxne.sxjdfreight.com/ne1/basedata/site_area_query.zul', headers=headers).text
        # print(part_r)

        part_body = r"'zul.inp.Textbox','(.*?)',{id:'txtSiteNameQ',"
        pattern_part = re.compile(part_body)
        sitename_code = re.findall(pattern_part, part_r)[0]

        dtid_body = "id:'pg_site_area_query',dt:'(.*?)'"
        pattern_dtid = re.compile(dtid_body)
        dtid = re.findall(pattern_dtid, part_r)[0]

        body_search = r"'zul.wgt.Button','(.*?)',{id:'btnSeach'"
        # 'zul.wgt.Button','bJiF4',{id:'btnSeach'
        pattern_search = re.compile(body_search)
        search_code = re.findall(pattern_search, part_r)[0]

        detail_body = r"'zul.sel.Listbox','(.*?)',{id:'lstbSiteList'"
        pattern_detail = re.compile(detail_body)
        detail_code = re.findall(pattern_detail, part_r)[0]

        phone_body = r"'zul.wgt.Label','(.*?)',.*?,value:'提货电话'"
        pattern_phone = re.compile(phone_body)
        phone_code = re.findall(pattern_phone, part_r)[0]

        sitename = cookie_item['site_name']
        data2 = {
            'dtid': dtid,
            'cmd_0': 'onChange',
            'uuid_0': sitename_code,
            'data_0': '{"value":'+'"'+sitename+'"'+',"start":'+str(len(sitename))+'}',
            'cmd_1': 'onBlur',
            'uuid_1': sitename_code,
        }

        headers2 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '177',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/basedata/site_area_query.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid),
        }
        r = requests.post(zk_url, data=data2, headers=headers2).text
        # print(r)

        data_search = {
            'dtid': dtid,
            'cmd_0': 'onClick',
            'uuid_0': search_code,
            'data_0': '{"pageX":66,"pageY":16,"which":1,"x":59,"y":14}',
        }

        headers_search = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '135',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/basedata/site_area_query.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1),
        }

        search_r = requests.post(zk_url, data=data_search, headers=headers_search).text
        # print(search_r)
        info_body = r'{label:"(.*?)"}'
        info_pattern = re.compile(info_body)
        info_list = re.findall(info_pattern, search_r)
        print(info_list[3])
        print(info_list[6])

        cli_body = "zul.sel.Listitem','(.*?)',{_loaded:true,_index:0}"
        cli_pattern = re.compile(cli_body)
        cli_code = re.findall(cli_pattern, search_r)[0]
        print(cli_code)

        data_cli = {
            'dtid': dtid,
            'cmd_0': 'onSelect',
            'uuid_0': detail_code,
            'data_0': '{"items":["' + str(cli_code) + '"],"reference":"' + str(
                cli_code) + '","clearFirst":false,"pageX":681,"pageY":266,"which":1,"x":375,"y":47}',
            'cmd_1': 'onClick',
            'uuid_1': detail_code,
            'data_1': '{"pageX":681,"pageY":266,"which":1,"x":375,"y":47}',
        }

        headers_cli = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '365',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/apps/index.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 1 + 1),
        }
        r_cli = requests.post(zk_url, data=data_cli, headers=headers_cli).text
        # print(r_cli)
        phone_data = {
            'dtid': dtid,
            'cmd_0': 'onClick',
            'uuid_0': detail_code,
            'data_0': '{"pageX":169,"pageY":226,"which":1,"x":158,"y":66}',
            'cmd_1': 'onDoubleClick',
            'uuid_1': detail_code,
            'data_1': '{"pageX":169,"pageY":226,"which":1,"x":158,"y":66}',
        }

        phone_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '270',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/apps/index.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'ZK-SID': str(sid + 3),
        }

        phone_r = requests.post(zk_url, data=phone_data, headers=phone_headers).text
        phonelist_body = r'"_value","(.*?)"'
        phonelist_pattern = re.compile(phonelist_body)
        phonelist = re.findall(phonelist_pattern, phone_r)
        print(phonelist)
        print('baseinfo*********************************')
        gLock.acquire()
        item_all['siteCode'] = info_list[0]
        item_all['siteType'] = info_list[3]
        item_all['siteStatus'] = info_list[6]
        item_all['franchisetime'] = info_list[18]
        item_all['phone'] = phonelist[10]
        item_all['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gLock.release()


#网点一级派送费
class F(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        psf_url = 'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul'
        headers = {
            'Cookie': cookie_item['cookies_jd'],
        }
        psf_r = requests.get(psf_url,headers=headers).text
        psf = psf_r.replace(r'\\"','"')
        # print(psf)
        print('yjpsf************************************')

        yfkjeBody  = r'"balance":"(.*?)",'
        pattern_yfk = re.compile(yfkjeBody)
        yfk = re.findall(pattern_yfk,psf)[1]
        # print(yfk)

        dtid_body = r"id:'.*?',dt:'(.*?)'"
        dtid_pattern = re.compile(dtid_body)
        dtid_code = re.findall(dtid_pattern,psf_r)[0]

        datesta_body = r"'zul.db.Datebox','(.*?)',{format:'yyyy/MM/dd',id:'dtbFinStart',"
        datesta_pattern = re.compile(datesta_body)
        datesta_code = re.findall(datesta_pattern,psf_r)[0]

        dateend_body = r"'zul.db.Datebox','(.*?)',{format:'yyyy/MM/dd',id:'dtbFinEnd'"
        dateend_pattern = re.compile(dateend_body)
        dateend_code = re.findall(dateend_pattern,psf_r)[0]


        datesea_body = r"'zul.wgt.Button','(.*?)',{id:'btnDetailSeach',"
        datesea_pattern = re.compile(datesea_body)
        datesea_code = re.findall(datesea_pattern,psf_r)[0]

        print(dtid_code)
        print(datesta_code)
        print(dateend_code)
        print(datesea_code)

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = date_list1 + date_list3
        print(ywdateend_list)

        yjyfkList = []
        for date in ywdateend_list:
            mon = "{}-{}".format(date[0],date[1])
            item = {}
            dfkData = {
            'dtid':dtid_code,
            'cmd_0':'onChange',
            'uuid_0':datesta_code,
            'data_0':'{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.1.0.0.0.0","start":10}',
            'cmd_1':'onChange',
            'uuid_1':dateend_code,
            'data_1':'{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                            date[2]) + '.23.59.59.0","start":10}',
            'cmd_2':'onClick',
            'uuid_2':datesea_code,
            'data_2':'{"pageX":75,"pageY":49,"which":1,"x":62,"y":11}',
            }

            dfk_headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'361',
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host':'sxne.sxjdfreight.com',
            'Origin':'http://sxne.sxjdfreight.com',
            'Referer':'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'ZK-SID':str(sid),
            }
            sid+=1


            dfk_r = requests.post(zk_url,data=dfkData,headers=dfk_headers).text
            # print(dfk_r)
            dfkBody = r',"value","(.*?)"'
            dfkPattern = re.compile(dfkBody)
            dfkList = re.findall(dfkPattern,dfk_r)
            print(dfkList[1])
            item['date'] = mon
            item['psf'] = dfkList[1]
            yjyfkList.append(item)
        gLock.acquire()
        item_all['yjpsfList'] = yjyfkList
        gLock.release()


#总体派送费
class G(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        sid = int((time.time() * 1000) % 9999 + 1)
        psf_url = 'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul'
        zk_url = 'http://sxne.sxjdfreight.com/zkau'
        headers = {
            'Cookie': cookie_item['cookies_jd'],
        }
        psf_r = requests.get(psf_url, headers=headers).text
        psf = psf_r.replace(r'\\"', '"')
        # print(psf)

        yfkjeBody = r'"balance":"(.*?)",'
        pattern_yfk = re.compile(yfkjeBody)
        yfk = re.findall(pattern_yfk, psf)[1]
        # print(yfk)

        dtid_body = r"id:'.*?',dt:'(.*?)'"
        dtid_pattern = re.compile(dtid_body)
        dtid_code = re.findall(dtid_pattern, psf_r)[0]

        datesta_body = r"'zul.db.Datebox','(.*?)',{format:'yyyy/MM/dd',id:'dtbFinStart',"
        datesta_pattern = re.compile(datesta_body)
        datesta_code = re.findall(datesta_pattern, psf_r)[0]

        dateend_body = r"'zul.db.Datebox','(.*?)',{format:'yyyy/MM/dd',id:'dtbFinEnd'"
        dateend_pattern = re.compile(dateend_body)
        dateend_code = re.findall(dateend_pattern, psf_r)[0]

        datesea_body = r"'zul.wgt.Button','(.*?)',{id:'btnDetailSeach',"
        datesea_pattern = re.compile(datesea_body)
        datesea_code = re.findall(datesea_pattern, psf_r)[0]

        site_body = r"'zul.inp.Textbox','(.*?)',{id:'txtFinOpenName',"
        site_pattern = re.compile(site_body)
        site_code = re.findall(site_pattern, psf_r)[0]

        tabBody = r"'zul.tab.Tab','(.*?)',{id:'tabFinInfo',"
        tab_pattern = re.compile(tabBody)
        tabCode = re.findall(tab_pattern, psf_r)

        print(dtid_code)
        print(datesta_code)
        print(dateend_code)
        print(datesea_code)
        print(site_code)
        print(tabCode)

        tabData = {
            'dtid': dtid_code,
            'cmd_0': 'onSelect',
            'uuid_0': tabCode,
            'data_0': '{"items":["' + tabCode[0] + '"],"reference":"' + tabCode[0] + '"}',
        }

        print('{"items":["' + tabCode[0] + '"],"reference":"' + tabCode[0] + '"}')

        tab_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '115',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'ZK-SID': str(sid),
        }

        r = requests.post(zk_url, data=tabData, headers=tab_headers).text
        # print(r)

        site_data = {
            'dtid': dtid_code,
            'cmd_0': 'onChanging',
            'opt_0': 'i',
            'uuid_0': site_code,
            'data_0': '{"value":"","start":0}',
        }

        site_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '101',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': cookie_item['cookies_jd'],
            'Host': 'sxne.sxjdfreight.com',
            'Origin': 'http://sxne.sxjdfreight.com',
            'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'ZK-SID': str(sid),
        }
        r = requests.post(zk_url, data=site_data, headers=site_headers).text
        # print(r)
        print('ztpsf*******************************************************')

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date_list1 = [[year, m, calendar.monthrange(year, m)[1]] for m in range(1, month)]
        date_list3 = [[year - 1, m, calendar.monthrange(year - 1, m)[1]] for m in range(month, 13)]
        ywdateend_list = date_list1 + date_list3
        print(ywdateend_list)

        ztyfkList = []
        for date in ywdateend_list:
            mon = "{}-{}".format(date[0], date[1])
            item = {}
            dfkData = {
                'dtid': dtid_code,
                'cmd_0': 'onChange',
                'uuid_0': datesta_code,
                'data_0': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.1.0.0.0.0","start":10}',
                'cmd_1': 'onChange',
                'uuid_1': dateend_code,
                'data_1': '{"value":"$z!t#d:' + str(date[0]) + '.' + str(date[1]) + '.' + str(
                    date[2]) + '.23.59.59.0","start":10}',
                'cmd_2': 'onClick',
                'uuid_2': datesea_code,
                'data_2': '{"pageX":75,"pageY":49,"which":1,"x":62,"y":11}',
            }
            sid += 1
            dfk_headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '361',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Cookie': cookie_item['cookies_jd'],
                'Host': 'sxne.sxjdfreight.com',
                'Origin': 'http://sxne.sxjdfreight.com',
                'Referer': 'http://sxne.sxjdfreight.com/ne1/finance/finance_detail_mgr_mini.zul',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                'ZK-SID': str(sid),
            }

            dfk_r = requests.post(zk_url, data=dfkData, headers=dfk_headers).text
            # print(dfk_r)
            dfkBody = r',"value","(.*?)"'
            dfkPattern = re.compile(dfkBody)
            dfkList = re.findall(dfkPattern, dfk_r)
            print(dfkList[1])
            item['date'] = mon
            item['psf'] = dfkList[1]
            ztyfkList.append(item)
        gLock.acquire()
        item_all['psfList'] = ztyfkList
        gLock.release()




class H(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        headers = {
            'Cookie': cookie_item['cookies_jd'],
        }
        index_url = 'http://sxne.sxjdfreight.com/apps/index.zul'
        index_r = requests.get(index_url,headers=headers).text
        indexBody = r"{id:'labEmployeeName',style:'color:white;',value:'(.*?)'}"
        index_pattern = re.compile(indexBody)
        username = re.findall(index_pattern,index_r)[0]
        gLock.acquire()
        item_all['user'] = username.strip("\\u3011")
        gLock.release()




def jd_spider(userid,company):
    with open('/home/xihonglin/Flask/testSiteCrawlApi/Spiders/jdcookies.json','r',encoding='utf-8') as f:
        cookies_item = json.loads(f.read())
        print(cookies_item)
    if cookie_item['code'] == 0:
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
        t8 = H()
        t8.start()

        t1.join()
        t2.join()
        t3.join()
        time.sleep(18)
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        item_all['userid'] = userid
        item_all['company'] = company

        return item_all
    else:
        return {'msg':'','code':600}



if __name__ == '__main__':
    item_all=jd_spider('18090014','sx198803.')
    print(json.dumps(item_all))
