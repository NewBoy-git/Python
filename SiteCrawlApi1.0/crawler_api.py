from flask import Flask, jsonify, request, render_template
# from Spiders.an_dxcspider import login_an
from Spiders.ymdd_dxcspider import ymdd_spider,ymddpart
from Spiders.baishi_dxcspider import baishi_spider
import json
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase.Hbase import Client, ColumnDescriptor, Mutation
from Spiders.an_slider_dxc import an_spider
from Spiders.anlb_dxc_spider import lb_spider

import time
app=Flask(__name__)

#爬虫程序接口
@app.route('/crawler/logistics',methods=['GET','POST'])
def crawl():
        sec = time.time()
        post_data = request.get_json()
        #print(post_data)
        obj = post_data
        if obj['entType'] == 'AN_NENG':
       	        username = obj['userName']
                password = obj['password']
                userid = obj['userId']
                company = obj['entType']
                socket.open()
                results = client.getRow('crawler:logistics_member_info',str(userid)+obj['entType'])
                socket.close()
                # if results:
                #    result = json.loads(results[0].columns.get('info:current').value)
                #    crawl_time = result['crawl_time']
                #    timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
                #    fir = int(time.mktime(timeArray))
                #    if sec-fir < 300:
                #       print(sec-fir)
                #       suc_msg = {
                #               "msg":"",
                #               "code":0,
                #               }
                #       return jsonify(suc_msg)
                #data = login_an(username,password)
                # c = CrackSlider()
                # data = c.crack_slider(username,password)
                data = lb_spider(username,password)
                if data['code'] == 600:
                   return jsonify(data)
                data['userid'] = userid
                data['company'] = company
                try:
                    socket.open()	   			
                    row =str(userid)+company
                    mutations = [Mutation(column="info:current", value=json.dumps(data))]
                    client.mutateRow(table, row, mutations)
                    socket.close()
                    suc_msg = {
                              "msg":"",
                              "code":0,
                              }
                    return jsonify(suc_msg)
                except Exception as e:
                    print(e)
                    error_hbase = {"msg":"","code":600}
                    return jsonify(error_hbase)
        if obj['entType'] == 'YI_MI_DI_DA':
                #print('YYYYYMMMMMDDDDDDDDD')
                username = obj['userName']
                password = obj['password']
                userid = obj['userId']
                company = obj['entType']
                com = obj['district']
                transport.open()
                results = client.getRow('crawler:logistics_member_info',str(userid)+obj['entType'])
                transport.close()
                if results:
                  result = json.loads(results[0].columns.get('info:current').value)
                  crawl_time = result['crawl_time']
                  timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
                  fir = int(time.mktime(timeArray))
                  if sec-fir < 300:
                     suc_msg = {
                             "msg":"",
                             "code":0,
                             }
                     return jsonify(suc_msg)
                ymdd_data = ymdd_spider(username,password,com)
                if ymdd_data['code'] == 600:
                    return jsonify(ymdd_data)
                #print(ymdd_data)
                ymdd_data['userid'] = userid
                ymdd_data['company'] = company
                try:
                    socket.open()
                    row = str(userid)+company
                    mutations = [Mutation(column="info:current", value=json.dumps(ymdd_data))]
                    client.mutateRow(table, row, mutations)
                    socket.close()
                    suc_msg = {
                    "msg":"",
                    "code":0,
                     }
                    return jsonify(suc_msg)
                except Exception as e:
                     print(e)
                     error_hbase = {"msg":"","code":600}
                     return jsonify(error_hbase)
        if obj['entType'] == 'BAI_SHI':
            username = obj['userName']
            password = obj['password']
            userid = obj['userId']
            company = obj['entType']
            socket.open()
            results = client.getRow('crawler:logistics_member_info',str(userid)+obj['entType'])
            socket.close()
            if results:
               result = json.loads(results[0].columns.get('info:current').value)
               crawl_time = result.get('crawl_time')
               if crawl_time != None:
                   timeArray = time.strptime(crawl_time, "%Y-%m-%d %H:%M:%S")
                   fir = int(time.mktime(timeArray))
                   if sec-fir < 300:
                       suc_msg = {
                              "msg":"",
                              "code":0,
                              }
                       return jsonify(suc_msg)
            baishi_data = baishi_spider(username,password)
            if baishi_data['code'] == 600:
                return jsonify(baishi_data)
            baishi_data['userid'] = userid
            baishi_data['company'] = company
            try:
                socket.open()
                row = str(userid) + company
                mutations = [Mutation(column="info:current", value=json.dumps(baishi_data))]
                client.mutateRow(table, row, mutations)
                socket.close()
                suc_msg = {
                    "msg": "",
                    "code": 0,
                }
                return jsonify(suc_msg)
            except Exception as e:
                print(e)
                error_hbase = {"msg":"","code":"600"}
                return jsonify(error_hbase)
#加工处理后的数据查询接口
@app.route('/select/logistics',methods=['POST'])
def select():
    userid = request.form.get('userid')
    if 'AN_NENG' in userid:
        socket.open()
        results = client.getRow('crawler:logistics_member_info', userid)
        socket.close()
        if results == []:
            msg = {'msg':'暂时查询不到该网点信息','code':1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
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
        # item['receiveBusiDetailSummaryVo'] = result['receiveBusiDetailSummaryVo']
        item['sendfirstfineBusiDetailSummaryVo'] = result['sendfineBusiDetailSummaryVo']['data']
        item['receivefirstfineBusiDetailSummaryVo'] = result['receivefineBusiDetailSummaryVo']['data']
        item['allfineBusiDetailSummaryVo'] = result['allfineBusiDetailSummaryVo']['data']
        item['userList'] = result['getUser']['data']['rows']
        item['Ywlist'] = result.get('yw_list')
        item['username'] = result.get('user')
        item['phone'] = result.get('phone')
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
        socket.open()
        results = client.getRow('crawler:logistics_member_info', userid)
        socket.close()
        if results == []:
            msg = {'msg': '暂时查询不到该网点信息', 'code': 1}
            return jsonify(msg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'BAI_SHI' in userid:
        socket.open()
        results = client.getRow('crawler:logistics_member_info', userid)
        socket.close()
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

if __name__=='__main__':
    socket = TSocket.TSocket('hb-bp1rh8i1frcu3a5s0-proxy-thrift.hbase.rds.aliyuncs.com',9099)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
    client = Client(protocol)
    table = 'crawler:logistics_member_info'
    app.run(host='0.0.0.0',port=11007,threaded = True)



