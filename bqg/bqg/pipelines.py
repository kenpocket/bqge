from itemadapter import ItemAdapter
import pymysql
from hashlib import md5
from dbutils.pooled_db import PooledDB


class BqgPipeline:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=0,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。
            # 如：0 = None = never,
            # 1 = default = whenever it is requested,
            # 2 = when a cursor is created,
            # 4 = when a query is executed,
            # 7 = always
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='novel_db',
            charset='utf8'
        )
        # self.con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456')
        # self.cursor = self.con.cursor()
        # self.cursor.execute('show databases;')
        # dbs = self.cursor.fetchall()
        # if ('novel_db',) not in dbs:
        #     self.cursor.execute('create database novel_db;')
        #     self.con.commit()
        # self.cursor.execute('use novel_db;')

    def process_item(self, item, spider):
        conn = self.pool.connection()
        cursor = conn.cursor()
        table_name = md5(item['novel_name'].encode()).hexdigest()
        sql = '''create table if not exists `{}`(
    `novel_url` varchar(300) not null unique ,
    `novel_name` text not null ,
    `novel_title` text not null ,
    `novel_content` text not null 
);'''.format(table_name)
        cursor.execute(sql)
        conn.commit()
        inst_sql = '''insert into `{}` (novel_url, novel_name, novel_title, novel_content)
values ('{}','{}','{}','{}');'''.format(table_name, *item.values())
        try:
            cursor.execute(inst_sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return item
