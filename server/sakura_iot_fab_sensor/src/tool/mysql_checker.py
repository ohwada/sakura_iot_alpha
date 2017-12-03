#!/usr/bin/env python

# Mysql Checker
# 2017-11-01 K.OHWADA

'''
This program, to monitor the life-and-death of Mysql server.
It is normal, that  the number of records in the specified table is 0 or more
If abnormal, this program restart themysql server and send the email.
'''
import subprocess
import smtplib
from email.mime.text import MIMEText
from mysql_base import Mysql

# class MysqlChecker
class MysqlChecker():
	
	INIT_D_CMD = "/etc/init.d/mysql"
	RESTART = "restart"
	MAIL_SUBJECT = "Restart Mysql Server"


# restartMysql
	def restartMysql(self):
		args = [ self.INIT_D_CMD, self.RESTART ]
		subprocess.Popen(args)
# ---

# sendmailMysql
	def sendmailMysql(self, to_addr):
		from_addr = to_addr
		body = self.MAIL_SUBJECT
		self.sendmail(from_addr, to_addr, self.MAIL_SUBJECT,  body )
# ---
	
	# sendmail
	def sendmail(self, from_addr, to_addr, subject, body):
		msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = from_addr
		msg['To'] = to_addr
		smtp = smtplib.SMTP()
		smtp.connect()
		smtp.sendmail(from_addr, [to_addr], msg.as_string())
		smtp.close()
# ---

#checkMysql
	def checkMysql(self, db_name, table, user, passwd):
		ret = False
		db = Mysql()
		conn = db.connect(db_name, user, passwd)	
		if not conn:	
			# print "connect error"	
			return False
		
			cnt = db.selectCount( table, "" )
			#	print "cnt: " + str(cnt)
	
			if cnt <= 0:
			#		print "cnt error"	
				return False
	
		return True
# ---

# class end
