
# SensorApi
# 2016-09-01 K.OHWDA

""" API

return The sensor data of the most recent one day  in the json format

Example of sensor data to be returned
------------------------
{
  "items": [
    {
      "humidity": 68.3828, 
      "light": 268.119, 
      "noise": 484.355, 
      "pressure": 1004.64, 
      "temperature": 13.9922, 
      "time": 1473513363
    }, 
        {
      "humidity": 73.181, 
      "light": 125.202, 
      "noise": 465.984, 
      "pressure": 978.914, 
      "temperature": 21.5058, 
      "time": 1473599703
    }
  ], 
  "num": 1440
}
  ---------------

"""

from sensor_db import SensorDb
from sensor_util import SensorUtil

# SensorApi
class SensorApi():
	SQL_WHERE = ""	
	SQL_ORDER_ID_DESC = "id DESC"
	SQL_OFFSET_NONE = 0 # no offset
	SQL_LIMIT_ONE_DAY = 24 * 60  # the number of data per day
	SEC_ONE_DAY = 24*60*60
	
	db = None
	db_param = None
	logger = None
	util = None

# init
	def __init__(self, db_param, logger):
		self.db_param = db_param
		self.logger = logger
# ---

# connect
	def connect(self):
		self.db = SensorDb()
		self.db.setLogger( self.logger )
		return self.db.connectParam( self.db_param )	
# ---

# close
	def close(self):
		self.db.close()
# ---

	# excute with psram
	# return result		
	def excute(self, param):
		conn = self.connect()
		if conn:
			rows = self.getLatestOneDay()
			self.close()			
		else:
			rows = []
		return self.buildResult(rows)
# ---

	# getLatestOneDay
	def getLatestOneDay(self):
		row_last = self.db.readLastOneTableItem()
		if row_last:
			end = row_last["time"]
			# on day ago
			start = end - self.SEC_ONE_DAY
			rows = self.db.readTableItemTime(start, end, self.SQL_LIMIT_ONE_DAY)
		else:
			rows = []	
		return rows
# ---

# buildResult
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
# ---

# buildItems
	def buildItems(self, num, rows):
		array = []
		for i in range(0, num):
			# reverse the order
			row = rows[ num - i  -1 ]
			array.append( self.buildItem(row) )
		return array;
# ---

# buildItem
	def buildItem(self, row):
		dict = {}
		dict["time"] = row["time"]
		dict["temperature"] = row["temperature"]
		dict["humidity"] = row["humidity"]
		dict["pressure"] = row["pressure"]
		dict["light"] = row["light"]
		dict["noise"] = row["noise"]
		return dict
# ---

# class end
