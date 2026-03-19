from conf.operationConfig import OperationConfig
import pymysql
from common.recordlog import logs
from pymysql.cursors import DictCursor
conf = OperationConfig()

class ConnectMysql:
    """
    操作MySQL数据库
    """

    def __init__(self):
        mysql_conf = {
            'host': conf.get_myswl_conf('host'),
            'port': int(conf.get_myswl_conf('port')),
            'user': conf.get_myswl_conf('user'),
            'password': conf.get_myswl_conf('password'),
            'database': conf.get_myswl_conf('database')
        }
        #链接mysql
        self.conn = pymysql.connect(**mysql_conf,charset='utf8')
        # cursor=pymysql.cursors.DictCursor 将结果返回字典类型
        #获取游标
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        # print(self.conn)

        logs.info("成功链接到数据库")
    #定义一个类，查询数据库
    def query(self,sql):
        """
        查询数据
        :param sql:
        :return:
        """
        try:
        #传入sql数据
            self.cursor.execute(sql)
        #进行提交sql
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
            #不管走哪一步，都会进行关闭
        finally:
            self.close()
    #定义关闭MySQL
    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()

if __name__ == '__main__':
    conn = ConnectMysql()
    sql = "select  deptno , avg(salary) avg_salary from emp where gender='female' group by deptno order by avg_salary desc"
    SQL2 = 'Alter table student drop sclass'
    print(conn.query(sql))

