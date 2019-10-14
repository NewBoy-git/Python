from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase.Hbase import Client, ColumnDescriptor, Mutation
import json

socket = TSocket.TSocket('hb-bp1rh8i1frcu3a5s0-proxy-thrift.hbase.rds.aliyuncs.com', 9099)
transport = TTransport.TBufferedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
client = Client(protocol)


#接口调用前查询方法    
def select_before(userid,company):
    table = 'crawler:test_logistics_member_info'
    socket.open()
    results = client.getRow(table, str(userid)+company)
    socket.close()
    return results


#hbase入库方法
def save_to_hbase(userid,company,data):
    table = 'crawler:test_logistics_member_info'
    socket.open()
    row = str(userid) + company
    mutations = [Mutation(column="info:current", value=json.dumps(data))]
    client.mutateRow(table, row, mutations)
    socket.close()
    suc_msg = {
        "msg": "",
        "code": 0,
    }
    return suc_msg


#查询接口hbase查询方法
def select_from_hbase(userid):
    socket.open()
    results = client.getRow('crawler:test_logistics_member_info', userid)
    socket.close()
    return results
        

    

