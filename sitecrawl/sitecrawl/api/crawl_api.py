import datetime
import json
import time
from concurrent.futures.thread import ThreadPoolExecutor

from flask import Blueprint, request, jsonify,current_app

from sitecrawl.HbaseHandler.operateHbase import save_to_hbase, select_before, select_from_hbase
from sitecrawl.MysqlHandler.status_table import update_status, acquire_status,incredit_status
from sitecrawl.Spiders.anlb_dxc_spider import CrackSlider, lb_spider
from sitecrawl.Spiders.baishi_dxcspider import baishi_spider
from sitecrawl.Spiders.jieda_ybdxcspider import jd_login, jd_spider
from sitecrawl.Spiders.ymdd_dxcspider import ymdd_spider, ymddpart
from ..config import Testingconfig

import logging
logger = logging.getLogger()

executor = ThreadPoolExecutor(1)

api = Blueprint('crawler',__name__,url_prefix='/crawler')


@api.route('/')
def index():
    return 'index'

@api.route('/logistics',methods=['GET','POST'])
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
                requesttype = obj['requestType']
                c = CrackSlider()
                cookies_item = c.crack_slider(username, password)
                if requesttype == 'UPGRADE_QUOTA':
                    try:
                        if cookies_item['code'] == 0:
                            update_status(userid, company, Testingconfig.waiting_status)
                            executor.submit(crawlan, userid, company,requesttype)
                            return jsonify(Testingconfig.success_msg)
                        else:
                            return jsonify(Testingconfig.error_msg)
                    except Exception as e:
                        print(e)
                        err_msg = {"msg": "", "code": 600}
                        return jsonify(err_msg)
                elif requesttype == 'IN_CREDIT_QUOTA':
                    try:
                        if cookies_item['code'] == 0:
                            incredit_status(userid, company, Testingconfig.waiting_status)
                            executor.submit(crawlan, userid, company,requesttype)
                            return jsonify(Testingconfig.success_msg)
                        else:
                            return jsonify(Testingconfig.error_msg)
                    except Exception as e:
                        print(e)
                        err_msg = {"msg": "", "code": 600}
                        return jsonify(err_msg)
                else:
                    try:
                        if cookies_item['code'] == 0:
                            acquire_status(userid, company, Testingconfig.waiting_status)
                            executor.submit(crawlan, userid, company,requesttype)
                            return jsonify(Testingconfig.success_msg)
                        else:
                           return jsonify(Testingconfig.error_msg)
                    except Exception as e:
                        print(e)
                        return jsonify(Testingconfig.error_msg)
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
                requesttype = obj['requestType']
                ymdd_data = ymdd_spider(username,password,com)
                if ymdd_data['code'] == 600:
                    if requesttype == 'UPGRADE_QUOTA':
                        update_status(userid, company, fail_status)
                    elif requesttype == "IN_CREDIT_QUOTA":
                        incredit_status(userid, company, fail_status)
                    else:
                        acquire_status(userid, company, fail_status)
                    return jsonify(ymdd_data)

                if requesttype == "UPGRADE_QUOTA":
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
                        update_status(userid, company, Testingconfig.success_status)
                        return jsonify(Testingconfig.success_msg)
                    except Exception as e:
                         print(e)
                         update_status(userid, company, Testingconfig.fail_status)
                         return jsonify(Testingconfig.error_msg)
                elif requesttype == "IN_CREDIT_QUOTA":
                    ymdd_data['userid'] = userid
                    ymdd_data['company'] = company
                    try:
                        save_to_hbase(userid, company, ymdd_data)
                        suc_msg = {
                            "msg": "",
                            "code": 0,
                        }
                        incredit_status(userid, company, Testingconfig.success_status)
                        return jsonify(suc_msg)
                    except Exception as e:
                        print(e)
                        incredit_status(userid, company, Testingconfig.fail_status)
                        error_hbase = {"msg": "", "code": 600}
                        return jsonify(error_hbase)
                else:
                    ymdd_data['userid'] = userid
                    ymdd_data['company'] = company
                    try:
                        save_to_hbase(userid, company, ymdd_data)
                        suc_msg = {
                            "msg": "",
                            "code": 0,
                        }
                        acquire_status(userid, company, Testingconfig.success_status)
                        return jsonify(suc_msg)
                    except Exception as e:
                        print(e)
                        acquire_status(userid, company, Testingconfig.fail_status)
                        error_hbase = {"msg": "", "code": 600}
                        return jsonify(error_hbase)

        if obj['entType'] == 'BAI_SHI':
            username = obj['userName']
            password = obj['password']
            userid = obj['userId']
            company = obj['entType']
            requesttype = obj['requestType']
            # transport.open()
            # results = client.getRow('crawler:test_logistics_member_info',str(userid)+obj['entType'])
            # transport.close()
            # results = select_before(userid, company)
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
                if requesttype == 'UPGRADE_QUOTA':
                    update_status(userid, company, fail_status)
                elif requesttype == "IN_CREDIT_QUOTA":
                    incredit_status(userid, company, fail_status)
                else:
                    acquire_status(userid, company, fail_status)
                return jsonify(baishi_data)

            if requesttype == 'UPGRADE_QUOTA':
                baishi_data['userid'] = userid
                baishi_data['company'] = company
                try:
                    suc_msg = save_to_hbase(userid,company,baishi_data)
                    update_status(userid, company, Testingconfig.success_status)
                    return jsonify(suc_msg)
                except Exception as e:
                    update_status(userid, company, Testingconfig.fail_status)
                    print(e)
                    error_hbase = {"msg":"","code":"600"}
                    return jsonify(error_hbase)
            elif requesttype == 'IN_CREDIT_QUOTA':
                baishi_data['userid'] = userid
                baishi_data['company'] = company
                try:
                    suc_msg = save_to_hbase(userid, company, baishi_data)
                    incredit_status(userid, company, Testingconfig.success_status)
                    return jsonify(suc_msg)
                except Exception as e:
                    incredit_status(userid, company, Testingconfig.fail_status)
                    print(e)
                    error_hbase = {"msg": "", "code": "600"}
                    return jsonify(error_hbase)
            else:
                baishi_data['userid'] = userid
                baishi_data['company'] = company
                try:
                    suc_msg = save_to_hbase(userid, company, baishi_data)
                    acquire_status(userid, company, Testingconfig.success_status)
                    return jsonify(suc_msg)
                except Exception as e:
                    acquire_status(userid, company, Testingconfig.fail_status)
                    print(e)
                    error_hbase = {"msg": "", "code": "600"}
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
                        return jsonify(Testingconfig.success_msg)
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
            requesttype = obj['requestType']
            cookie_item = jd_login(username, password)
            if requesttype == 'UPGRADE_QUOTA':
                try:
                    if cookie_item['code'] == 0:
                        update_status(userid, company, Testingconfig.waiting_status)
                        executor.submit(crawljd, userid, company,requesttype)
                        return jsonify(Testingconfig.success_msg)
                    else:
                        return jsonify(Testingconfig.error_msg)
                except Exception as e:
                    print(e)
                    err_msg = {"msg": "", "code": 600}
                    return jsonify(err_msg)
            elif requesttype == 'IN_CREDIT_QUOTA':
                try:
                    if cookie_item['code'] == 0:
                        incredit_status(userid, company, Testingconfig.waiting_status)
                        executor.submit(crawljd, userid, company,requesttype)
                        return jsonify(Testingconfig.success_msg)
                    else:
                        return jsonify(Testingconfig.error_msg)
                except Exception as e:
                    print(e)
                    err_msg = {"msg": "", "code": 600}
                    return jsonify(err_msg)
            else:
                try:
                    if cookie_item['code'] == 0:
                        acquire_status(userid, company, Testingconfig.waiting_status)
                        executor.submit(crawljd, userid, company,requesttype)
                        return jsonify(Testingconfig.success_msg)
                    else:
                        return jsonify(Testingconfig.error_msg)
                except Exception as e:
                    print(e)
                    return jsonify(Testingconfig.error_msg)


def crawljd(userid,company,requesttype):
        print("异步执行crawljd")
    # with current_app.app_context():
        if requesttype == 'UPGRADE_QUOTA':
            try:
                sta1 = datetime.datetime.now()
                item = jd_spider(userid, company)
                sta2 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid,company,item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end - sta2))
                print('流程总耗时:{}'.format(end - sta1))
                print('****************************************************')
                update_status(userid, company, Testingconfig.success_status)
                print(suc_msg)
            except Exception as e:
                if 'Working outside of request context' not in str(e):
                    update_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                else:
                    print(str(e))
        elif requesttype == 'IN_CREDIT_QUOTA':
            try:
                sta1 = datetime.datetime.now()
                item = jd_spider(userid, company)
                sta2 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid,company,item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end - sta2))
                print('流程总耗时:{}'.format(end - sta1))
                print('****************************************************')
                incredit_status(userid, company, Testingconfig.success_status)
                print(suc_msg)
            except Exception as e:
                if 'Working outside of request context' not in str(e):
                    incredit_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                else:
                    print(str(e))
        else:
            try:
                sta1 = datetime.datetime.now()
                item = jd_spider(userid, company)
                sta2 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid,company,item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end - sta2))
                print('流程总耗时:{}'.format(end - sta1))
                print('****************************************************')
                acquire_status(userid, company, Testingconfig.success_status)
                print(suc_msg)
            except Exception as e:
                if 'Working outside of request context' not in str(e):
                    acquire_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                    # error_hbase = {"msg":"","code":600}
                    # return jsonify(error_hbase)
                else:
                    print(str(e))


# @copy_current_request_context
# with app.app_context():
#     print(app.name)
def crawlan(userid,company,requesttype):
        print('异步执行crawlan')
    # with app.app_context():
        if requesttype == 'UPGRADE_QUOTA':
            try:
                print('************************')
                item = lb_spider(userid, company)
                sta1 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid,company,item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end-sta1))
                print('流程总耗时:{}'.format(end-sta1))
                update_status(userid, company, Testingconfig.success_status)
                return jsonify(suc_msg)
            except Exception as e:
                if 'Working outside of application context' not in str(e):
                    update_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                    # error_hbase = {"msg":"","code":600}
                    # return jsonify(error_hbase)
                else:
                    print(str(e))
        elif requesttype == 'IN_CREDIT_QUOTA':
            try:
                item = lb_spider(userid, company)
                sta1 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid,company,item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end-sta1))
                print('流程总耗时:{}'.format(end-sta1))
                incredit_status(userid, company, Testingconfig.success_status)
                return jsonify(suc_msg)
            except Exception as e:
                if 'Working outside of application context' not in str(e):
                    incredit_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                    # error_hbase = {"msg":"","code":600}
                    # return jsonify(error_hbase)
                else:
                    print(str(e))
        else:
            try:
                sta1 = datetime.datetime.now()
                item = lb_spider(userid, company)
                sta2 = datetime.datetime.now()
                suc_msg = save_to_hbase(userid, company, item)
                end = datetime.datetime.now()
                print('入库总耗时:{}'.format(end - sta2))
                print('流程总耗时:{}'.format(end - sta1))
                incredit_status(userid, company, Testingconfig.success_status)
                return jsonify(suc_msg)
            except Exception as e:
                if 'Working outside of application context' not in str(e):
                    incredit_status(userid, company, Testingconfig.fail_status)
                    print(str(e))
                    print('************************')
                    # error_hbase = {"msg":"","code":600}
                    # return jsonify(error_hbase)
                else:
                    print(str(e))

#壹米滴答大区列表接口、
@api.route('/logisticsDistrict',methods=['POST'])
def ympart():
    post_data = request.get_json()
    obj = post_data
    if obj['entType'] =='YI_MI_DI_DA':
       data = ymddpart()
       logger.debug('info')
       return jsonify(data)


