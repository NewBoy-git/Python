import pymysql
from ..config import Testingconfig



def update_status(userid,company,status):
    connect = pymysql.connect(
        host=Testingconfig.MYSQL_HOST,
        db=Testingconfig.MYSQL_DB,
        user=Testingconfig.MYSQL_USER,
        passwd=Testingconfig.MYSQL_PASSWORD,
        charset='utf8',
        use_unicode=Testingconfig.USE_UNICODE
    )
    cursor = connect.cursor()

    print(userid,Testingconfig.company_map[company],status)

    sql = "UPDATE upgrade_quota_material set {}='{}' WHERE user_id ={};".format(Testingconfig.company_map[company],status,userid)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    cursor.close()

def acquire_status(userid,company,status):
    connect = pymysql.connect(
        host=Testingconfig.MYSQL_HOST,
        db=Testingconfig.MYSQL_DB,
        user=Testingconfig.MYSQL_USER,
        passwd=Testingconfig.MYSQL_PASSWORD,
        charset='utf8',
        use_unicode=Testingconfig.USE_UNICODE
    )
    cursor = connect.cursor()

    print(userid, Testingconfig.company_map[company], status)

    sql = "UPDATE acquire_quota_material set {}='{}' WHERE user_id ={};".format(Testingconfig.company_map[company], status, userid)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    cursor.close()


def incredit_status(userid,company,status):
    connect = pymysql.connect(
        host=Testingconfig.MYSQL_HOST,
        db=Testingconfig.MYSQL_DB,
        user=Testingconfig.MYSQL_USER,
        passwd=Testingconfig.MYSQL_PASSWORD,
        charset='utf8',
        use_unicode=Testingconfig.USE_UNICODE
    )
    cursor = connect.cursor()
    print(userid, Testingconfig.company_map[company], status)

    sql = "UPDATE in_credit_quota_material set {}='{}' WHERE user_id ={};".format(Testingconfig.company_map[company],
                                                                                status, userid)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    cursor.close()
    
    
