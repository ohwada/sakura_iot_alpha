# SensorUtil
# 2016-07-01 K.OHWADA

from logging.handlers import RotatingFileHandler
import logging
import os
import shutil
import json
import dateutil.parser
import datetime
import time

class SensorUtil():

	TIME_ZONE = 9 # JST (UTC+9)

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

	def initBasedir(self, param_basedir, appname):
		if param_basedir is not None:
			basedir = param_basedir
		else:
			basedir = os.path.expanduser(os.path.join("~", "." + appname.lower()))
		self.makeDirsIfNotExist( basedir )
		return basedir

	def initConfig(self, basedir):
		src = self.getSrcPath( "conf", "user.conf" )
		dst = self.getDstPath( basedir, "conf", "user.conf" )
		self.copyFile(src, dst)
		return dst

	def getSrcPath(self, subdir, name):
    		dir_self = os.path.dirname(__file__)
		dir_conf = os.path.join( dir_self, subdir )
 		path = os.path.join( dir_conf, name )
		return path

	def getDstPath(self, basedir, subdir, name):
		dst_dir = self.makeSubDir( basedir, subdir )
 		return os.path.join( dst_dir, name )

	def makeSubDir(self, basedir, subdir):
		path = os.path.join( basedir, subdir )
		self.makeDirsIfNotExist( path )
		return path

	def makeDirsIfNotExist(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)

	def copyFile(self, src, dst):
		if not os.path.exists(dst):
        		shutil.copyfile(src, dst)

	def initLogFileHandler(self, basedir):
		dir_logs = self.makeSubDir( basedir, 'logs' )
		debug_file_handler = self.makeFileHandler( dir_logs, 'debug.log', logging.DEBUG )
		error_file_handler = self.makeFileHandler( dir_logs, 'error.log', logging.ERROR )
		return [debug_file_handler, error_file_handler]

	def makeFileHandler(self, dir_logs, name, level):
		formatter = logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'
		)
		path = os.path.join( dir_logs, name )
		handler = RotatingFileHandler(
			path, maxBytes=100000, backupCount=10
		)
		handler.setLevel( level )
		handler.setFormatter( formatter )
		return handler

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

# class end
