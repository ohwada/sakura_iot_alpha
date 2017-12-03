#!/usr/bin/env python

# ServerChecker
# 2016-09-01 K.OHWADA

'''
This program, to monitor the life-and-death of Sakura IoT Fab Sensor server.
It is normal, that the unixtime sent back from the server and the current time of this program matches.
If abnormal, this program restart the server and send the email.
'''

import urllib2
import datetime
import time
import subprocess
import smtplib
from email.mime.text import MIMEText

# ServerChecker
class ServerChecker():

	URL = "http://localhost:5050/status"
	CMD_INIT_D = "/etc/init.d/sakura-iot-fab-sensor"
	RESTART =  "restart"
	DIFFERENCE = 10 # 10 sec
	MAIL_SUBJECT = "Restart Sakura Iot Server"

# checkServer
	def checkServer(self):
		return self.checkServerUnixtime( self.URL)
# ---

# checkServerUnixtime
	def checkServerUnixtime(self, url):
		ret = False
		unix_get = 0
		try:
			response = urllib2.urlopen(url)
			unix_get = int( response.read() )
			# print unix_get
		except:
			pass
		unix_now = self.getUnixtimeNow()
		if abs(unix_now - unix_get) < self.DIFFERENCE:
			#  match
			ret = True
		return ret
# ---

# getUnixtimeNow
	def getUnixtimeNow(self):
		now = datetime.datetime.now()
		unix = int(time.mktime(now.timetuple()))
		return unix
# ---

# restartServer
	def restartServer(self):
		args = [ self.CMD_INIT_D, self.RESTART ]
		subprocess.Popen(args)
# ---

# sendmailServer
	def sendmailServer(self,  to_addr):
		from_addr = to_addr
		subject = self.MAIL_SUBJECT
		body = self.MAIL_SUBJECT
		self.sendmail(from_addr, to_addr, subject, body)
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

# class end