#!/usr/bin/env python

# check my sql server
# 201-11-01 K.OHWADA

'''
This program, to monitor the life-and-death of Mysql server.
It is normal, that  the number of records in the specified table is 0 or more
If abnormal, this program restart themysql server and send the email.
'''

import urllib2
import datetime
import time
import subprocess
import smtplib
from email.mime.text import MIMEText

from mysql_base import MysqlBase

# --- your setting ---
MYSQL_USER = "your mysql user"
MYSQL_PASSWD = "your mysql passwd"
MYSQL_DB = "your mysql db name"
MYSQL_TABLE	= "your mysql table  name"
MAIL_FROM = "your_from_email_address"
MAIL_TO = "your_to_email_address" 
# ---

MAIL_SUBJECT = "Restart Mysql Server"
MAIL_BODY = MAIL_SUBJECT

def restart():
	args1 = ["/etc/init.d/mysql", "restart"]
	subprocess.Popen(args1)
# ---
	
def sendmail(from_addr, to_addr, subject, body):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = from_addr
	msg['To'] = to_addr
	smtp = smtplib.SMTP()
	smtp.connect()
	smtp.sendmail(from_addr, [to_addr], msg.as_string())
	smtp.close()
# ---

#check
def check():
	ret = False
	db = MysqlBase()
	conn = db.connect(MYSQL_DB, MYSQL_USER, MYSQL_PASSWD)
	
	if not conn:	
		print "connect error"	
		return False
		
	cnt = db.selectCount( MYSQL_TABLE, "" )
#	print "cnt: " + str(cnt)
	if cnt <= 0:
#		print "cnt error"	
		return False
	
	return True
# ---


# main
print "check mysql server"
ret = check()
# if abnormal, restart and send mail
if not ret:
	print "mysql error"
	restart()
	sendmail(MAIL_FROM, MAIL_TO, MAIL_SUBJECT, MAIL_BODY)
print "mysql ok"
