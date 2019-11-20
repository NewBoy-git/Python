from flask import Blueprint, request, jsonify

from sitecrawl.HbaseHandler.operateHbase import save_to_hbase

from ..config import Testingconfig


sav = Blueprint('savehbase',__name__,url_prefix='/savehbase')

@sav.route('/logistics',methods=['GET','POST'])
def save_hbase():
    item=request.get_json()
    # print(item)
    userid = item.get('userId')
    company = item.get('company')
    if userid and company:
        try:
            suc_msg = save_to_hbase(userid,company,item)
            print(suc_msg)
            return jsonify(suc_msg)
        except Exception as e:
            print(e)
            error_hbase = {"msg": "", "code": 600}
            print(error_hbase)
            return jsonify(error_hbase)
    else:
        return jsonify(Testingconfig.error_msg)
