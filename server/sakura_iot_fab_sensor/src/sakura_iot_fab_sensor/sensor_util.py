# SensorUtil
# 2016-07-01 K.OHWADA

from sensor_db import SensorDb
import os
import shutil
import json
import dateutil.parser
import datetime
import time

class SensorUtil():

	TIME_ZONE = 9 # JST (UTC+9)
		
	def connect(self, name, user, passwd, timeout):
		db = SensorDb()
		# wait for connect
		# because MySQL is not started
		# when the power is turned on
		end = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
		while(True):
			ret = db.connect( name, user, passwd )
			# break, if connected
			if ret: break
			time.sleep(1)
			if datetime.datetime.now() > end:
				# return, if timeover
				print "DB error: not connect"
				return  None
		# while end
		db.createTableItemIfNotExist()
		return db

	def readConf(self, path):        
    		if os.path.exists(path):
    			f = open(path)
			obj = json.load(f)
			f.close()
        		return obj
		return None

	def initParam(self, param, default):
		if param is not None:
			val = param
		else:
			val = default
		return val

	def initConfig(self, basedir):
		src = self.getSrcPath("conf", "user.conf")
		dst = self.getDstPath(basedir, "user.conf")
		self.copyFile(src, dst)
		return dst

	def initBasedir(self, param_basedir, appname):
		if param_basedir is not None:
			basedir = param_basedir
		else:
			basedir = os.path.expanduser(os.path.join("~", "." + appname.lower()))
		if not os.path.isdir(basedir):
			os.makedirs(basedir)
		return basedir

	def getSrcPath(self, subdir, name):
    		dir_self = os.path.dirname(__file__)
		dir_conf = os.path.join( dir_self, subdir )
 		path = os.path.join( dir_conf, name )
		return path
    	
	def getDstPath(self, basedir, name):
 		return os.path.join( basedir, name )
    
	def copyFile(self, src, dst):
		if not os.path.exists(dst):
        		shutil.copyfile(src, dst)

	def makeJsDate(self, time):
		str_time = str ( ( time + 3600 * self.TIME_ZONE) * 1000 )
		date = "new Date(" + str_time  + ")" 
		return date

	def getUnixtimeNow(self):
		now = datetime.datetime.now()
		unix = int(time.mktime(now.timetuple()))
		return unix

	def getFormatTime(self, unixtime, format ):
		dt = datetime.datetime.fromtimestamp( unixtime )
		# UTC -> Local
		local = dt + datetime.timedelta( hours=self.TIME_ZONE )
		return local.strftime( format )

	def convUnixtime(self, text):
		dt = dateutil.parser.parse(text)
		unix = int(time.mktime(dt.timetuple()))
		return unix

# class end
