# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from hashlib import md5

class BqgPipeline:
    def __init__(self):
        self.con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456')
        self.cursor = self.con.cursor()
        self.cursor.execute('show databases;')
        dbs = self.cursor.fetchall()
        if ('novel_db',) not in dbs:
            self.cursor.execute('create database novel_db;')
            self.con.commit()
        self.cursor.execute('use novel_db;')

    def process_item(self, item, spider):
        table_name = md5(item['novel_name'].encode()).hexdigest()
        sql = '''create table if not exists {}(
    `novel_url` text not null ,
    `novel_name` text not null ,
    `novel_title` text not null ,
    `novel_content` text not null 
);
        '''.format(table_name)
        cursor = self.con.cursor()
        cursor.execute(sql)
        self.con.commit()
        inst_sql = '''insert into `1aca8488d14e6920b0e8a9617e05a4d8` (novel_url, novel_name, novel_title, novel_content)
values ('{}','{}','{}','{}');
        '''.format(*item.values())
        cursor.execute(inst_sql)
        self.con.commit()
        return item
