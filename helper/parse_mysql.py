from config import *
import pymysql


class parse_mysql:
    def __init__(self):
        self.user = MYSQL_USER
        self.passwd = MYSQL_PASSWD
        self.ip = MYSQL_IP
        self.port = MYSQL_PORT
        self.con = pymysql.connect(host=self.ip, port=self.port, user=self.user, password=self.passwd)
