#!/usr/bin/env python

# check server
# 2016-09-01 K.OHWADA

'''
This program, to monitor the life-and-death of Sakura IoT Fab Sensor server.
It is normal, that the unixtime sent back from the server and the current time of this program matches.
If abnormal, this program restart the server and send the email.
'''

from sakura_iot_server_checker import ServerChecker
from server_conf import ServerConf

# --- your setting ---
USER = "ohwada"
APPNAME = "sakura_iot_fab_sensor"

# main
print "check server"
checker = ServerChecker()
conf = ServerConf()
param = conf. readConf( USER, APPNAME  )
if not param:
	print "conf error"
ret = checker.checkServer()
if  not ret:
	# error
	print "server error"
	checker.restartServer()
	checker.sendmailServer(param["email"])
