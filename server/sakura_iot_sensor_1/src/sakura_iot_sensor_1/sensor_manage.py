# SensorManage
# 2016-07-01 K.OHWDA

from sensor_db import SensorDb
from sensor_util import SensorUtil
import random

# SensorManage
class SensorManage():
	SQL_WHERE = ""	
	SQL_ORDER = "DESC"
	SQL_OFFSET = 0
	SQL_LIMIT = 50
	TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

	db = None
	util = None

	def __init__(self, db):
		self.db = db
		self.util = SensorUtil()

	def makeList(self, args):			
		return self.getList()

	def makeAddForm(self, args):
		cols = self.db.makeFormTableItem( 0, 0, 0, 0, 0, 0, 0 )
		params = { "action":"add", "id":0, "cols":cols }
		return params

	def makeEditForm(self, args):
		id = args.get('id', '0')
		if id <= 0:
			error = "invalid id: " + str(id)
			print error
			params = { "action":"", "id":0, "cols":{}, "error":error }
			return params
		row = self.db.readTableItemById( id )
		if not row:
			error = "invalid data id=" + str(id)
			print error
			params = { "action":"", "id":0, "cols":{}, "error":error }
			return params			
		cols = self.db.makeFormTableItem( \
			row["time"], row["module"], row["temperature"], row["humidity"], row["pressure"], row["light"], row["noise"] )
		params = { "action":"edit", "id":id, "cols":cols }
		return params

	def post(self, form):
		action = str(form['action'])
		print "action " + action
		if action == "add":
			self.addRecord(form)
		elif action == "edit":
			self.editRecord(form)
		elif action == "delete":
			id = int(form['id'])
			self.db.deleteTableItem( id )
		elif action == "delete_all":
			self.db.deleteAllTableItem()
		elif action == "gen_data":
			self.generateData()
		return self.getList()

	def addRecord(self, form):
		time = int(form['time'])
		module = str(form['module'])
		temp = float(form['temperature'])
		humi = float(form['humidity'])
		pressure = float(form['pressure'])
		light = float(form['light'])
		noise = float(form['noise'])
		self.db.insertTableItem( time, module, temp, humi, pressure, light, noise )

	def editRecord(self, form):
		id = int(form['id'])
		time = int(form['time'])
		module = str(form['module'])
		temp = float(form['temperature'])
		humi = float(form['humidity'])
		pressure = float(form['pressure'])
		light = float(form['light'])
		noise = float(form['noise'])
		self.db.updateTableItem( id, time, module, temp, humi, pressure, light, noise )

	def getList(self):
		rows = self.db.readAllTableItem( self.SQL_WHERE, self.SQL_ORDER, self.SQL_LIMIT, self.SQL_OFFSET )
		if not rows:
			print self.db.getError()
		new_rows = []	
		for row in rows:
			row["formated_time"] = self.util.getFormatTime( row["time"], self.TIME_FORMAT )
			new_rows.append(row)	
		return new_rows

	def generateData(self):
		now = self.util.getUnixtimeNow()
		start = now - 400 * 24 * 60  * 60 # one year ago
		module = "abc"
		values = [0, 0, 0, 0, 0]
		mins = [10,  30, 950, 100, 400]
		maxs = [30, 80, 1050, 300, 600]
		divs = [20, 50, 1000, 200, 500]
		# create data of one minute interval
		for time in range(start, now, 60):			
			# make five values
			for i in range(0, 5):
				v = values[i]
				v += divs[i]
				if v < mins[i]:					
					# invert div, when smaller
					v = mins[i]
					divs[i] = random.uniform(0.05, 1.0)
				elif v > maxs[i]:
					# invert div, when bigger
					v = maxs[i]
					divs[i] = - random.uniform(0.05, 1.0)
				values[i] = v
			# for i end			
			self.db.insertTableItem( time, module, values[0], values[1], values[2], values[3], values[4] )
		# for time end

# class end
