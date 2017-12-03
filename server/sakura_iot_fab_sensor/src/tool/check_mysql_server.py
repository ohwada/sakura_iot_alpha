#!/usr/bin/env python

# check mysql server
# 2017-11-01 K.OHWADA

'''
This program, to monitor the life-and-death of Mysql server.
It is normal, that  the number of records in the specified table is 0 or more
If abnormal, this program restart themysql server and send the email.
'''


from mysql_checker import MysqlChecker
from server_conf import ServerConf

# --- your setting ---
USER = "ohwada"
APPNAME = "sakura_iot_fab_sensor"
MYSQL_TABLE = "iot_item"


# ---



# main
print "check mysql server"
conf = ServerConf()
param = conf. readConf( USER, APPNAME  )
print param
if not param:
	print "conf error"
checker = MysqlChecker()
ret = checker.checkMysql( param["db_name"], MYSQL_TABLE, param["db_user"], param["db_passwd"])

# if abnormal, restart and send mail
if not ret:
	print "mysql error"
	checker.restartMysql()
	checker.sendmailMysql(param["email"])
