
#通用配置：
class config(object):
    #hbase配置，测试和线上一个数据库、
    HBASE_HOST = 'hb-bp1rh8i1frcu3a5s0-proxy-thrift.hbase.rds.aliyuncs.com'
    HBASE_PORT = 9099

    #异步状态信息
    success_status = "SUCCEED"
    fail_status = "FAILED"
    waiting_status = "WAITING"

    #mysql数据字段映射
    company_map = {
        "AN_NENG": "anneng_tms_state",
        "YI_MI_DI_DA": "yimi_tms_state",
        "BAI_SHI": "baishi_tms_state",
        "SHUN_XIN_JIE_DA": "shunxin_tms_state"
    }

    #接口返回信息：
    error_msg = {"msg": "", "code": 600}
    success_msg = {"msg": "", "code": 0}

    #查询接口返回：
    nullmsg = {'msg':'暂时查询不到该网点信息','code':1}



#测试环境配置
class Testingconfig(config):
    #测试环境hbase表
    HBASE_TABLE = 'crawler:test_logistics_member_info'

    #测试环境mysql连接配置
    MYSQL_HOST = '47.110.49.102'
    MYSQL_DB = 'credit_system_zhiguo'
    MYSQL_USER = 'credit'
    MYSQL_PASSWORD = 'credit@Huayijia1009'
    CHARSET = 'utf8'
    USE_UNICODE = True



#线上环境配置
class Onlineconfig(config):
    # 线上环境hbase表
    Hbase_TABLE = 'crawler:logistics_member_info'

    #线上环境mysql连接配置
    MYSQL_HOST = 'rm-bp1y2ov8bthirn4up.mysql.rds.aliyuncs.com'
    MYSQL_DB = 'credit_system'
    MYSQL_USER = 'credit'
    MYSQL_PASSWORD = 'credit@Huayijia1009'
    CHARSET = 'utf8'
    USE_UNICODE = True


config_map = {
    'testing':Testingconfig
}


