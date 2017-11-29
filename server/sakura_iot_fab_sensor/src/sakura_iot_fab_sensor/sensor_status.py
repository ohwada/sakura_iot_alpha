# SensorStatus
# 2016-09-01 K.OHWDA

""" status

return the status of the server.
It is used to monitor the server's life and death.
If it is normal, return the unix time of the current time

"""

from sensor_db import SensorDb
from sensor_util import SensorUtil

# SensorStatus
class SensorStatus():

	db_param = None
	logger = None

	def __init__(self, db_param, logger):
		self.db_param = db_param
		self.logger = logger

	def excute(self):
		db = SensorDb()
		db.setLogger( self.logger )
		ret = db.connectParam( self.db_param )	
		if ret:
			# connect to DB
			count = db.countTableItemTimeAll()
			db.close()
			if count == 0:
				# if reocord not exits, return 0
				return 0
			else:
				# if reocord exits, return unixtime
				util = SensorUtil()	
				return str(util.getUnixtimeNow())
		# others, return error code,
		return -1
			
# class end
