import json

from flask import Flask, jsonify, request

from phone_cap import phone_cap
from spider import baidu_search

app=Flask(__name__)

@app.route('/baidu',methods=['GET'])
def baidui():
    phone_str = request.args.get('phone')
    phone_list = phone_str.split(',')
    phone = phone_list[0]
    data = baidu_search(phone)

    return jsonify(data)

@app.route('/phonecap',methods=['GET'])
def phonecap():
    phone_str = request.args.get('phone')
    phone_list = phone_str.split(',')
    phone = phone_list[0]
    data = phone_cap(phone)
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


if __name__=='__main__':
    app.run(host='0.0.0.0',port=11010,threaded = True,debug=True)
