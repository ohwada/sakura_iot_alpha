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

# class SensorUtil
class SensorUtil():

	TIME_ZONE = 9 # JST (UTC+9)

# initParam
	def initParam(self, param, default):
		if param is not None:
			val = param
		else:
			val = default
		return val
# ---

# initBasedir
	def initBasedir(self, param_basedir, appname):
		if param_basedir is not None:
			basedir = param_basedir
		else:
			basedir = os.path.expanduser(os.path.join("~", "." + appname.lower()))
		self.makeDirsIfNotExist( basedir )
		return basedir
# ---

# initConfig
	def initConfig(self, basedir):
		src = self.getSrcPath( "conf", "user.conf" )
		dst = self.getDstPath( basedir, "conf", "user.conf" )
		self.copyFile(src, dst)
		return dst
# ---

# getSrcPath
	def getSrcPath(self, subdir, name):
    		dir_self = os.path.dirname(__file__)
		dir_conf = os.path.join( dir_self, subdir )
 		path = os.path.join( dir_conf, name )
		return path
# ---

# getDstPath
	def getDstPath(self, basedir, subdir, name):
		dst_dir = self.makeSubDir( basedir, subdir )
 		return os.path.join( dst_dir, name )
# ---

# makeSubDir
	def makeSubDir(self, basedir, subdir):
		path = os.path.join( basedir, subdir )
		self.makeDirsIfNotExist( path )
		return path
# ---

# makeDirsIfNotExist
	def makeDirsIfNotExist(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)
# ---

# copyFile
	def copyFile(self, src, dst):
		if not os.path.exists(dst):
        		shutil.copyfile(src, dst)
# ---

# initLogFileHandler
	def initLogFileHandler(self, basedir):
		dir_logs = self.makeSubDir( basedir, 'logs' )
		debug_file_handler = self.makeFileHandler( dir_logs, 'debug.log', logging.DEBUG )
		error_file_handler = self.makeFileHandler( dir_logs, 'error.log', logging.ERROR )
		return [debug_file_handler, error_file_handler]
# ---

# makeFileHandler
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
# ---

# makeJsDate
	def makeJsDate(self, time):
		str_time = str ( ( time + 3600 * self.TIME_ZONE) * 1000 )
		date = "new Date(" + str_time  + ")" 
		return date
# ---

# getUnixtimeNow
	def getUnixtimeNow(self):
		now = datetime.datetime.now()
		unix = int(time.mktime(now.timetuple()))
		return unix
# ---

# getFormatTime
	def getFormatTime(self, unixtime, format ):
		dt = datetime.datetime.fromtimestamp( unixtime )
		# UTC -> Local
		local = dt + datetime.timedelta( hours=self.TIME_ZONE )
		return local.strftime( format )
# ---

# class end
