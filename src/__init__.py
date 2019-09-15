from flask import Flask, escape, request
# For using on macOs, MySQLClient cannot be installed correctly...
# import MySQLdb
import pymysql

pymysql.install_as_MySQLdb()

from . import config
from .views import *

app = Flask(__name__)

conf = config.get_config()
db_conf = conf['db']
db_conn = MySQLdb.connect(
    host=db_conf['host'],
    user=db_conf['user'],
    passwd=db_conf['passwd'],
    db=db_conf['db'],
    port=db_conf['port'],
)



