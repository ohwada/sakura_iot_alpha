# SensorMain
# 2016-07-01 K.OHWDA

from sensor_db import SensorDb
from sensor_util import SensorUtil

# SensorMain
class SensorMain():
	RANGE_PERIOD = "period"
#	RANGE_DAY = "day"
	RANGE_WEEK = "week"
	RANGE_MONTH = "month"
	RANGE_YEAR = "year"
	SEC_DAY = 24 * 60 * 60 # one day in seconds
	SEC_WEEK = 7 * SEC_DAY # one week
	SEC_MONTH = 30 * SEC_DAY # one month	
	SEC_YEAR = 365 * SEC_DAY	# one year
	SQL_WHERE = ""	
	SQL_ORDER = "DESC"
	SQL_OFFSET = 0 # no offset
	SQL_LIMIT = 24 * 60  # the number of data per day
	DATE_FORMAT = "%Y-%m-%d %H:%M"
	
	db = None
	util = None

	def __init__(self, db):
		self.db = db
		self.util = SensorUtil()

	def excute(self, args):
		range = args.get('r', '')
		start_in = args.get('s', '')
		end_in = args.get('e', '')
		datas = ['', '', '']
		dt = ""
		error = ""
		ret = self.getRecordsTimeRange( range, start_in, end_in )
		if len(ret) > 0:
			# valid data
			count  = ret["count"]
			rows = ret["rows"]			
			dt = self.getHeaderDateTime( count, rows ) 
			datas = self.makeChartData( rows )
		else:
			# no data
			error = "No Data"
		param = { "datas":datas, "datetime":dt, "error":error }
		return param

	def getRecordsTimeRange(self, range, start_in, end_in ):
		start, end = self.calcPeriodTime( range, start_in, end_in )
		count = self.db.countTableItemTime( start, end )
		if count == 0:
			# read the latest data, if no data in the time range
			rows0 = self.db.readAllTableItem( self.SQL_WHERE, self.SQL_ORDER, self.SQL_LIMIT, self.SQL_OFFSET )
			len0 = len(rows0)
			if len0 > 0:
			# data exists
				ret0 = { "count":len0, "rows":rows0 }
				return ret0
		elif count <= self.SQL_LIMIT:
			# reads the data, If within the limit
			rows1 = self.db.readTableItemTime( start, end, self.SQL_LIMIT)
			ret1 = { "count":count, "rows":rows1 }
			return ret1
		# read out thinning, if exceeds the limit
		skip2 = int( count / self.SQL_LIMIT )
		rows2 = self.db.readTableItemTimeSkip( start, end, skip2, 2 * self.SQL_LIMIT )
		ret2 = { "count":count, "rows":rows2 }
		return ret2
						
	def calcPeriodTime(self, range, start_in, end_in ):
		if range == self.RANGE_PERIOD:
			# convert start time and end time	
			# when specify "period"
			start = self.util.convUnixtime( start_in )
			end  = self.util.convUnixtime( end_in )
			return [ start, end ]
		elif range == self.RANGE_WEEK:
			# convert one week in seconds
			# when specify "week"
			sec = self.SEC_WEEK
		elif range == self.RANGE_MONTH:
			# convert one month in seconds
			sec = self.SEC_MONTH		
		elif range == self.RANGE_YEAR:
			# convert one year in seconds
			sec = self.SEC_YEAR	
		else:
			# convert one day in seconds
			sec = self.SEC_DAY
		end = self.util.getUnixtimeNow()
		start = end - sec
		return [ start, end ]
			
	def getHeaderDateTime(self, count, rows ):
		length = len( rows )
		first = rows[0]["time"]
		last = rows[ length - 1 ]["time"]
		str_count = str(length)
		if length < count:			
			# display the original number of data
			# if skipped data
			str_count = str(length) + " / " + str(count)
		text = "DateTime "
		# start time
		text += self.util.getFormatTime( last, self.DATE_FORMAT )
		text += " - "
		# end time
		text += self.util.getFormatTime( first, self.DATE_FORMAT )	
		text += " ( "
		text += str_count
		text += " )"
		return text

	def makeChartData(self, rows):
		# data0 : temperature and humidity
		# data1 : light and noise
		# data2 : pressure
		data0 = "["
		data1 = "["
		data2 = "["
		length = len(rows)
		isFirst = True
		for i in range(0, length):
			# reverse the order
			row = rows[ length - i  -1 ]
			date = self.util.makeJsDate( row["time"]  )
			if isFirst:
				isFirst = False
			else:
				data0 += ", "
				data1 += ", "	
				data2 += ", "	
			data0 += "[" + date  + "," + str(row["temperature"]) + "," + str(row["humidity"]) + "]"
			data1 += "[" + date  + "," + str(row["light"]) + "," + str(row["noise"]) + "]"
			data2 += "[" + date  + "," + str(row["pressure"]) + "]"
		data0 += "]"
		data1 += "]"
		data2 += "]"
		return [data0, data1, data2]

# class end