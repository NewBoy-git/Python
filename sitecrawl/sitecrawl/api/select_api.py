#加工处理后的数据查询接口
import json

from flask import request, jsonify, Blueprint

from sitecrawl.HbaseHandler.operateHbase import select_from_hbase

from ..config import Testingconfig

sel = Blueprint('select',__name__,url_prefix='/select')


@sel.route('/logistics',methods=['POST'])
def select():
    userid = request.form.get('userid')
    if 'AN_NENG' in userid:
        results = select_from_hbase(userid)
        if results == []:
            return jsonify(Testingconfig.nullmsg)
        result = json.loads(results[0].columns.get('info:current').value)
        # print(result)
        # print(result['ThismonthendsyesterdayBusiQuery'])
        item = {}
        item['siteName'] = result['site_name']
        item['siteType'] = result['site_type']
        item['siteId'] = result['site_id']
        item['siteCode'] = result.get('siteCode')
        item['company'] = result['company']
        item['userId'] = result['userid']
        item['crawlTime'] = result['crawl_time']
        item['accountInfo'] = result['AccountInfo']['data']
        item['busidetailByMonth'] = result['BusiDetailByMonth']
        if result.get('sendBusiDetailSummaryVo'):
            item['sendfirstBusiDetailSummaryVo'] = result.get('sendBusiDetailSummaryVo').get('data')
        else:
            item['sendfirstBusiDetailSummaryVoList']  = result.get('sendfirstBusiDetailSummaryVoList')
        #item['receiveBusiDetailSummaryVo'] = result['receiveBusiDetailSummaryVo']

        item['sendfirstfineBusiDetailSummaryVoList'] = result.get('sendfirstfineBusiDetailSummaryVoList')
        item['receivefirstfineBusiDetailSummaryVoList'] = result.get('receivefineBusiDetailSummaryVoList')
        item['allfineBusiDetailSummaryVoList'] = result.get('allfineBusiDetailSummaryVoList')

        if  result.get('sendfineBusiDetailSummaryVo'):
            item['sendfirstfineBusiDetailSummaryVo'] = result.get('sendfineBusiDetailSummaryVo').get('data')
        else:
            item['sendfirstfineBusiDetailSummaryVo'] = result.get('sendfineBusiDetailSummaryVo')

        if result.get('receivefineBusiDetailSummaryVo'):
            item['receivefirstfineBusiDetailSummaryVo'] = result.get('receivefineBusiDetailSummaryVo').get('data')
        else:
            item['receivefirstfineBusiDetailSummaryVo'] = result.get('receivefineBusiDetailSummaryVo')

        if result.get('allfineBusiDetailSummaryVo'):
            item['allfineBusiDetailSummaryVo'] = result.get('allfineBusiDetailSummaryVo').get('data')
        else:
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
        # return jsonify(result)

    if 'YI_MI_DI_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            return jsonify(Testingconfig.nullmsg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'BAI_SHI' in userid:
        results = select_from_hbase(userid)
        if results == []:
            return jsonify(Testingconfig.nullmsg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    if 'YUN_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            return jsonify(Testingconfig.nullmsg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)


    if 'SHUN_XIN_JIE_DA' in userid:
        results = select_from_hbase(userid)
        if results == []:
            return jsonify(Testingconfig.nullmsg)
        result = json.loads(results[0].columns.get('info:current').value)
        return jsonify(result)

    return jsonify(Testingconfig.nullmsg)
