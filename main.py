import httpx
import config
import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor
url = 'https://www.xbiquge.so/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-HK;q=0.6,ug;q=0.5,ja;q=0.4,hmn;q=0.3,ko;q=0.2,ia;q=0.1,ar;q=0.1,de;q=0.1,fr;q=0.1,ru;q=0.1,ms;q=0.1,my;q=0.1,ne;q=0.1,pt;q=0.1,th;q=0.1,es;q=0.1,it;q=0.1,vi;q=0.1',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


class MysqlTaskPool(PooledDB):
    __instance = None
    # 连接池对象
    __pool = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # cls.__instance = object.__new__(cls)
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, db_name, host, user, passwd):
        """创建链接池"""
        PooledDB.__init__(
            self, pymysql, maxconnections=80, mincached=0, maxcached=0, maxshared=0, blocking=True,
            host=host, port=3306, database=db_name,
            user=user, password=passwd,
            # user='root', password='soar123',
            charset='utf8mb4', cursorclass=DictCursor
        )

    def __del__(self):
        PooledDB.close(self)

    def conn(self):
        _conn = self.connection()
        return _conn
