#!/usr/bin/env python

# check server
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

# --- your setting ---
URL = "http://localhost:5050/status"
MAIL_FROM = "your_from_email_address"
MAIL_TO = "your_from_email_address" 
# ---

MAIL_SUBJECT = "Restart Sakura Iot Server"
MAIL_BODY = MAIL_SUBJECT
MAIL_SUBJECT_KEEP = "Sakura Iot Server"

def getUnixtimeNow():
	now = datetime.datetime.now()
	unix = int(time.mktime(now.timetuple()))
	return unix

def restart():
	args = ["/etc/init.d/sakura-iot-fab-sensor", "restart"]
	subprocess.Popen(args)

def sendmail(from_addr, to_addr, subject, body):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = from_addr
	msg['To'] = to_addr
	smtp = smtplib.SMTP()
	smtp.connect()
	smtp.sendmail(from_addr, [to_addr], msg.as_string())
	smtp.close()

# main
print "check server"
unix_get = 0
try:
	response = urllib2.urlopen(URL)
	unix_get = int( response.read() )
except:
	pass
unix_now = getUnixtimeNow()
if unix_get < unix_now - 60 or unix_get > unix_now + 60:
	# if abnormal, restart and send mail
	restart()
	sendmail(MAIL_FROM, MAIL_TO, MAIL_SUBJECT, MAIL_BODY)
#else:
#	when normal, to send mail
#	sendmail(MAIL_FROM, MAIL_TO, MAIL_SUBJECT_KEEP, MAIL_SUBJECT_KEEP)
