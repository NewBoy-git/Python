import pymysql



def update_status(userid,company,status):
    connect = pymysql.connect(
        host='rm-bp1y2ov8bthirn4up.mysql.rds.aliyuncs.com',
        db='credit_system',
        user='credit',
        passwd='credit@Huayijia1009',
        charset='utf8',
        use_unicode=True
    )
    cursor = connect.cursor()
    company_map = {
        "AN_NENG":"anneng_tms_state",
        "YI_MI_DI_DA":"yimi_tms_state",
        "BAI_SHI":"baishi_tms_state",
        "SHUN_XIN_JIE_DA":"shunxin_tms_state"
    }
    print(userid,company_map[company],status)

    sql = "UPDATE upgrade_quota_material set {}='{}' WHERE user_id ={};".format(company_map[company],status,userid)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    cursor.close()

def acquire_status(userid,company,status):
    connect = pymysql.connect(
        host='rm-bp1y2ov8bthirn4up.mysql.rds.aliyuncs.com',
        db='credit_system',
        user='credit',
        passwd='credit@Huayijia1009',
        charset='utf8',
        use_unicode=True
    )
    cursor = connect.cursor()
    company_map = {
        "AN_NENG": "anneng_tms_state",
        "YI_MI_DI_DA": "yimi_tms_state",
        "BAI_SHI": "baishi_tms_state",
        "SHUN_XIN_JIE_DA": "shunxin_tms_state"
    }
    print(userid, company_map[company], status)

    sql = "UPDATE acquire_quota_material set {}='{}' WHERE user_id ={};".format(company_map[company], status, userid)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    cursor.close()

    
    
