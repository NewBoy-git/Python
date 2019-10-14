#!/usr/bin/env python
# -*- coding: utf-8 -*-


#pytho系统包
import time
import json
import datetime

#第三方包、
from flask import Flask, jsonify, request, render_template
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase.Hbase import Client, ColumnDescriptor, Mutation
from concurrent.futures import ThreadPoolExecutor
# from gevent.monkey import patch_all


#模块自身包
from Spiders.ymdd_dxcspider import ymdd_spider,ymddpart
from Spiders.baishi_dxcspider import baishi_spider
# from Spiders.an_slider import an_spider
from HbaseHandler.operateHbase import save_to_hbase,select_before,select_from_hbase
from MysqlHandler.status_table import update_status
from Spiders.bdjs import baidu_search
from Spiders.phone_cap import phone_search
# from Spiders.yunda_spider import yunda_spider
from Spiders.anlb_dxc_spider import lb_spider,CrackSlider
# from Spiders.anlb_ybspider import CrackSlider,lb_spider

from Spiders.jd_dxc_spider import jd_login,jd_spider
import calendar


# patch_all()

executor = ThreadPoolExecutor(1)


app=Flask(__name__)

error_msg = {"msg": "", "code": 600}

success_status = "SUCCEED"
fail_status = "FAILED"
waiting_status = "WAITING"


#爬虫程序接口
@app.route('/crawler/logistics',methods=['GET','POST'])
def crawl():
        sta = datetime.datetime.now()
        sec = time.time()
        post_data = request.get_json()
        obj = post_data
        if obj['entType'] == 'AN_NENG':
       	        username = obj['userName']
                password = obj['password']
                userid = obj['userId']
                company = obj['entType']
        #         results = select_before(userid,company)
        #         if results:
        #            result = json.loads(results[0].columns.get('info:current').value)
        #            crawl_time = result['crawl_time']
        #            timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
        #            fir = int(time.mktime(timeArray))
        #            if sec-fir < 300:
        #               suc_msg = {
        #                       "msg":"",
        #                       "code":0,
        #                       }
        #               return jsonify(suc_msg)
        #         c = CrackSlider()
        #         data = c.crack_slider(username,password)
                c = CrackSlider()
                cookies_item = c.crack_slider(username, password)
                try:
                    if cookies_item['code'] == 0:
                        update_status(userid, company, waiting_status)
                        executor.submit(crawlan, userid, company)
                        suc_msg = {"msg": "", "code": 0}
                        return jsonify(suc_msg)
                    else:
                        err_msg = {"msg": "", "code": 600}
                        return jsonify(err_msg)

                except Exception as e:
                    print(e)
                    err_msg = {"msg": "", "code": 600}
                    return jsonify(err_msg)
        #         err_msg = {"msg": "", "code": 600}
        #         return jsonify(err_msg)
        #         data = lb_spider(username,password)
        #         if data['code'] == 600:
        #            return jsonify(data)
        #         data['userid'] = userid
        #         data['company'] = company
        #         try:
        #             sta1 = datetime.datetime.now()
        #             suc_msg = save_to_hbase(userid,company,data)
        #             end = datetime.datetime.now()
        #             print('入库总耗时:{}'.format(end-sta1))
        #             print('流程总耗时:{}'.format(end-sta))
        #             return jsonify(suc_msg)
        #         except Exception as e:
        #             print(e)
        #             error_hbase = {"msg":"","code":600}
        #             return jsonify(error_hbase)

        if obj['entType'] == 'YI_MI_DI_DA':
                username = obj['userName']
                password = obj['password']
                userid = obj['userId']
                company = obj['entType']
                com = obj['district']
                ymdd_data = ymdd_spider(username,password,com)
                if ymdd_data['code'] == 600:
                    return jsonify(ymdd_data)
                #print(ymdd_data)
                ymdd_data['userid'] = userid
                ymdd_data['company'] = company
                try:
                    # transport.open()
                    # row = str(userid)+company
                    # mutations = [Mutation(column="info:current", value=json.dumps(ymdd_data))]2
                    # client.mutateRow(table, row, mutations)
                    # transport.close()
                    save_to_hbase(userid,company,ymdd_data)
                    suc_msg = {
                    "msg":"",
                    "code":0,
                     }
                    update_status(userid,company,success_status)
                    return jsonify(suc_msg)
                except Exception as e:
                     print(e)
                     update_status(userid, company, fail_status)
                     error_hbase = {"msg":"","code":600}
                     return jsonify(error_hbase)
        if obj['entType'] == 'BAI_SHI':
            username = obj['userName']
            password = obj['password']
            userid = obj['userId']
            company = obj['entType']
            # transport.open()
            # results = client.getRow('crawler:test_logistics_member_info',str(userid)+obj['entType'])
            # transport.close()
            results = select_before(userid, company)
            # if results:
            #    result = json.loads(results[0].columns.get('info:current').value)
            #    crawl_time = result.get('crawl_time')
            #    if crawl_time != None:
            #       timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
            #       fir = int(time.mktime(timeArray))
            #       if sec-fir < 300:
            #           print(sec-fir)
            #           suc_msg = {
            #                   "msg":"",
            #                   "code":0,
            #                   }
            #           update_status(userid, company, success_status)
            #           return jsonify(suc_msg)
            baishi_data = baishi_spider(username,password)
            if baishi_data['code'] == 600:
                return jsonify(baishi_data)
            baishi_data['userid'] = userid
            baishi_data['company'] = company
            try:
                suc_msg = save_to_hbase(userid,company,baishi_data)
                update_status(userid, company, fail_status)
                return jsonify(suc_msg)
            except Exception as e:
                update_status(userid, company, fail_status)
                print(e)
                error_hbase = {"msg":"","code":"600"}
                return jsonify(error_hbase)
        if obj['entType'] == 'YUN_DA':
            username = obj['userName']
            password = obj['password']
            userid = obj['userId']
            company = obj['entType']
            results = select_before(userid, company)
            if results:
                result = json.loads(results[0].columns.get('info:current').value)
                crawl_time = result.get('crawl_time')
                if crawl_time != None:
                    timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
                    fir = int(time.mktime(timeArray))
                    if sec - fir < 300:
                        print(sec - fir)
                        suc_msg = {
                            "msg": "",
                            "code": 0,
                        }
                        return jsonify(suc_msg)
            yunda_data = yunda_spider(username, password)
            if yunda_data['code'] == 600:
                return jsonify(yunda_data)
            yunda_data['userid'] = userid
            yunda_data['company'] = company
            try:
                suc_msg = save_to_hbase(userid, company, yunda_data)
                return jsonify(suc_msg)
            except Exception as e:
                print(e)
                error_hbase = {"msg": "", "code": "600"}
                return jsonify(error_hbase)

        if obj['entType'] == 'SHUN_XIN_JIE_DA':
            username = obj['userName']
            password = obj['password']
            userid = obj['userId']
            company = obj['entType']
            cookie_item = jd_login(username, password)
            try:
                if cookie_item['code'] == 0:
                    executor.submit(crawljd, userid, company)
                    suc_msg = {"msg": "", "code": 0}
                    return jsonify(suc_msg)
            except Exception as e:
                print(e)
                err_msg = {"msg": "", "code": 600}
                return jsonify(err_msg)
            err_msg = {"msg": "", "code": 600}
            return jsonify(err_msg)

def crawljd(userid,company):
    app.app_context().push()
    # sta = time.time()
    item = jd_spider(userid,company)
    print(item)
    # end = time.time()
    # print(end-sta)
    try:
        if item['code'] == 0:
            suc_msg = save_to_hbase(userid,company,item)
            print('****************************************************')
            print(suc_msg)
            return jsonify(suc_msg)
        else:
            return jsonify(error_msg)
    except Exception as e:
        print(e)
        error_hbase = {"msg": "", "code": 600}
        return jsonify(error_hbase)

def crawlan(userid,company):
    with app.app_context():

    # sec = datetime.time().now()
        item=lb_spider(userid,company)
        # end = datetime.time().now()
        # print('采集总耗时',end-sec)
        # userid = item['userid']
        # company = item['company']
        try:
            sta1 = datetime.datetime.now()
            suc_msg = save_to_hbase(userid,company,item)
            end = datetime.datetime.now()
            print('入库总耗时:{}'.format(end-sta1))
            print('流程总耗时:{}'.format(end-sta1))
            update_status(userid, company, success_status)
            return jsonify(suc_msg)
        except Exception as e:
            print(e)
            error_hbase = {"msg":"","code":600}
            return jsonify(error_hbase)



#加工处理后的数据查询接口
@app.route('/select/logistics',methods=['POST'])
def select():
    userid = request.form.get('userid')
    if 'AN_NENG' in userid:
        results = select_from_hbase(userid)
        if results == []:
            msg = {'msg':'暂时查询不到该网点信息','code':1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
        # print(result)
        # print(result['ThismonthendsyesterdayBusiQuery'])
        item = {}
        item['siteName'] = result['site_name']
        item['siteType'] = result['site_type']
        item['siteId'] = result['site_id']
        item['company'] = result['company']
        item['userId'] = result['userid']
        item['crawlTime'] = result['crawl_time']
        item['accountInfo'] = result['AccountInfo']['data']
        item['busidetailByMonth'] = result['BusiDetailByMonth']
        item['sendfirstBusiDetailSummaryVo'] = result['sendBusiDetailSummaryVo']['data']
        #item['receiveBusiDetailSummaryVo'] = result['receiveBusiDetailSummaryVo']
        item['sendfirstfineBusiDetailSummaryVo'] = result.get('sendfineBusiDetailSummaryVo')
        item['receivefirstfineBusiDetailSummaryVo'] = result.get('receivefineBusiDetailSummaryVo')
        item['allfineBusiDetailSummaryVo'] = result.get('allfineBusiDetailSummaryVo')
        item['userList'] = result['getUser']['data']['rows']
        item['ywList'] = result.get('yw_list')
        item['username'] = result.get('user')
        item['phone'] = result.get('phone')
        item['yjList'] = result.get('yj_list')
        item['franchisetime'] = result.get('franchisetime')
        #item['finAccountList'] = result['finAccountList']
        yesterdayBusiQuery = {}
        yesterdayBusiQuery_items = result['yesterdayBusiQuery']
        BusiQuery_map = {
            "发货费":"deliveryCharges",
            "付派件费":"payfordIspatch",
            "充值":"reCharge",
            "到付款":"paymentbyArrival",
            "代收货款":"collectionofGoods",
            "物料费":"materialCost",
            "罚款":"fine",
            "增值费":"valueaddedFee",
            "网点费用申请":"applicationforNetworkFee",
            "充值手续费":"rechargeCharges",
            #"其他往来":"otherExpenses",
        }
        categroy_list = ["发货费","付派件费","充值","到付款","代收货款", "物料费","罚款","增值费","网点费用申请","充值手续费"]
        xy_list = []
        for i in range(0,len(yesterdayBusiQuery_items)):
            xy_list.append(yesterdayBusiQuery_items[i]['category'])
            if yesterdayBusiQuery_items[i]['category'] in categroy_list:
               yesterdayBusiQuery[BusiQuery_map[yesterdayBusiQuery_items[i]['category']]]= yesterdayBusiQuery_items[i]['sold'] #发货费
        for j in categroy_list:
            if j  in categroy_list and j not in xy_list:
               yesterdayBusiQuery[BusiQuery_map[j]] = 0
        item['yesterdayBusiQuery'] = yesterdayBusiQuery
        ThismonthendsyesterdayBusiQuery = {}
        ThismonthendsyesterdayBusiQuery_items = result['ThismonthendsyesterdayBusiQuery']
        xm_list = []
        for i in range(0,len(ThismonthendsyesterdayBusiQuery_items)):
            xm_list.append(ThismonthendsyesterdayBusiQuery_items[i]['category'])
            if ThismonthendsyesterdayBusiQuery_items[i]['category'] in categroy_list:
               ThismonthendsyesterdayBusiQuery[BusiQuery_map[ThismonthendsyesterdayBusiQuery_items[i]['category']]] = ThismonthendsyesterdayBusiQuery_items[i]['sold']  # 发货费
        for k in categroy_list:
            if k in categroy_list and k not in xm_list:
               ThismonthendsyesterdayBusiQuery[BusiQuery_map[k]] = 0
        item['thismonthendsyesterdayBusiQuery'] = ThismonthendsyesterdayBusiQuery
        item['code']=0
        return jsonify(item)

    if 'YI_MI_DI_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            msg = {'msg': '暂时查询不到该网点信息', 'code': 1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'BAI_SHI' in userid:
        results = select_from_hbase(userid)
        if results == []:
            msg = {'msg': '暂时查询不到该网点信息', 'code': 1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'YUN_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            msg = {'msg': '暂时查询不到该网点信息', 'code': 1}
            return msg
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'SHUN_XIN_JIE_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            msg = {'msg': '暂时查询不到该网点信息', 'code': 1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

#壹米滴答大区列表接口、
@app.route('/crawler/logisticsDistrict',methods=['POST'])
def ympart():
    post_data = request.get_json()
    obj = post_data
    if obj['entType'] =='YI_MI_DI_DA':
       data = ymddpart()
       return jsonify(data)

#百度检索记录
@app.route('/baidu',methods=['GET'])
def baidui():
    phone_str = request.args.get('phone')
    phone_list = phone_str.split(',')
    phone = phone_list[0]
    data = baidu_search(phone)
    return jsonify(data)

#百度安全号码标记记录、、
@app.route('/phonecap',methods=['GET'])
def phonecap():
    phone_str = request.args.get('phone')
    phone_list = phone_str.split(',')
    phone = phone_list[0]
    data = phone_search(phone)
    obj = json.loads(data)
    if type(obj['data']['list'])==list:
        data = {
            'count':len(obj['data']['list']),
            'name': obj['data']['list'][0].get('name'),
            'address':obj['data']['list'][0].get('address'),
            'type':'baidu'

        }
    else:
        data = {
            'count': 0,
            'name': "",
            "address":"",
            'type':'baidu'

        }
    return jsonify(data)

@app.route('/savehbase/logistics',methods=['GET','POST'])
def save_hbase():
    item=request.get_json()
    # print(item)
    userid = item['userId']
    company = item['company']
    try:
        suc_msg = save_to_hbase(userid,company,item)
        print(suc_msg)
        return jsonify(suc_msg)
    except Exception as e:
        print(e)
        error_hbase = {"msg": "", "code": 600}
        print(error_hbase)
        return jsonify(error_hbase)



if __name__=='__main__':
    app.run(host='0.0.0.0',port=11010,threaded = True)



