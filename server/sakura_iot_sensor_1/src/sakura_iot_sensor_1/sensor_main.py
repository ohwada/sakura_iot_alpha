# SensorMain
# 2016-07-01 K.OHWDA

from sensor_db import SensorDb
from sensor_util import SensorUtil

# SensorMain
class SensorMain():
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
		start1, end1 = self.calcPeriodTime( range, start_in, end_in )
		count1 = self.db.countTableItemTime( start1, end1 )
		if (count1 > 0) and (count1 <= self.SQL_LIMIT):
			# reads the data, If within the limit
			rows1 = self.db.readTableItemTime( start1, end1, self.SQL_LIMIT)
			ret = { "count":count1, "rows":rows1 }
			return ret
		elif count1 > self.SQL_LIMIT:
			# read out thinning, if exceeds the limit
			skip2 = int( count1 / self.SQL_LIMIT )
			rows2 = self.db.readTableItemTimeSkip( start1, end1, skip2, 2 * self.SQL_LIMIT )
			ret = { "count":count1, "rows":rows2 }
			return ret
		else:
			# read the latest data, if no data in the time range
			rows3 = self.db.readAllTableItem( self.SQL_WHERE, self.SQL_ORDER, self.SQL_LIMIT, self.SQL_OFFSET )
			len3 = len(rows3)
			if len3 > 0:
				# data exists
				ret = { "count":len3, "rows":rows3 }
				return ret
		# return empty, if no data		
		return {}

	def calcPeriodTime(self, range, start_in, end_in ):
		if range == "period":
			# convert start time and end time	
			# when specify "period"
			start = self.util.convUnixtime( start_in )
			end  = self.util.convUnixtime( end_in )
			return [ start, end ]
		elif range == "week":
			# convert one week in seconds
			# when specify "week"
			sec = self.SEC_WEEK
		elif range == "month":
			# convert one month in seconds
			sec = self.SEC_MONTH		
		elif range == "year":
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
