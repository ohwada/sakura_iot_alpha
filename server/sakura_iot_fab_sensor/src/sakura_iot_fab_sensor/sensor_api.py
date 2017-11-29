# SensorApi
# 2016-09-01 K.OHWDA

""" API

return The sensor data of the most recent one day  in the json format

"""

from sensor_db import SensorDb
from sensor_util import SensorUtil

# SensorApi
class SensorApi():
	SQL_WHERE = ""	
	SQL_ORDER_ID_DESC = "id DESC"
	SQL_OFFSET_NONE = 0 # no offset
	SQL_LIMIT_ONE_DAY = 24 * 60  # the number of data per day

	db = None
	db_param = None
	logger = None
	util = None

	def __init__(self, db_param, logger):
		self.db_param = db_param
		self.logger = logger

	def connect(self):
		self.db = SensorDb()
		self.db.setLogger( self.logger )
		return self.db.connectParam( self.db_param )	

	def close(self):
		self.db.close()

	# return result		
	def excute(self, param):
		conn = self.connect()
		if conn:
			# connect to DB	
			rows = self.db.readAllTableItem( self.SQL_WHERE, self.SQL_ORDER_ID_DESC, self.SQL_LIMIT_ONE_DAY, self.SQL_OFFSET_NONE )
			self.close()
		else:
			# if reocord exits, return unixtime
			rows = []
		return self.buildResult(rows)

	def buildResult(self, rows):
		num = len(rows)
		if num > 0:
			array = self.buildItems(num, rows)
		else:
			array = ""
		dict = {}
		dict["num"] = num
		dict["items"] = array
		return dict

	def buildItems(self, num, rows):
		array = []
		for i in range(0, num):
			# reverse the order
			row = rows[ num - i  -1 ]
			array.append( self.buildItem(row) )
		return array;

	def buildItem(self, row):
		dict = {}
		dict["time"] = row["time"]
		dict["temperature"] = row["temperature"]
		dict["humidity"] = row["humidity"]
		dict["pressure"] = row["pressure"]
		dict["light"] = row["light"]
		dict["noise"] = row["noise"]
		return dict

# class end
