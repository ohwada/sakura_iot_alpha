# SensorDb
# 2016-07-01 K.OHWDA

from sensor_db_base import SensorDbBase

# SensorDb
class SensorDb(SensorDbBase):
	ORDER_DESC = "DESC"
	ORDER_ASC = "ASC"
	OFFSET_ZERO = 0
	LIMIT_NONE = 0
	LIMIT_ONE = 1
	TIME_NUM = 1000
	TABLE_ITEM = "iot_item"

	def createTableItemIfNotExist(self):
		if not self.existsTable( self.TABLE_ITEM ):
			ret = self.createTableItem()
			if not ret:
				# stop program, if error
				exit()
			print "Created table " + self.TABLE_ITEM

	def createTableItem(self):
		sql = "CREATE TABLE " + self.TABLE_ITEM
    		sql += " ( "
    		sql += " id INT NOT NULL AUTO_INCREMENT, "
    		sql += " time INT, "
    		sql += " module TEXT, "
    		sql += " temperature FLOAT, "
    		sql += " humidity FLOAT, "
    		sql += " pressure FLOAT, "
    		sql += " light FLOAT, "
    		sql += " noise FLOAT, "
    		sql += " PRIMARY KEY (id) "
    		sql += " ) "
    		return self.execute( sql ) 

	def countTableItemTimeAll(self):	
		return self.selectCount( self.TABLE_ITEM, "" )

	def countTableItemTime(self, start, end):	
		where = self.buildTimeWhere( start, end )
		return self.selectCount( self.TABLE_ITEM, where )

	def readTableItemById(self, id):
		return self.selectOneById( self.TABLE_ITEM, id )

	def readAllTableItem(self, where, order, limit, offset):
		return self.selectAll( self.TABLE_ITEM, where, order, limit, offset )

	def readTableItemTime(self,  start, end, limit):	
		where = self.buildTimeWhere( start, end )
		return self.selectAll( self.TABLE_ITEM, where, self.ORDER_DESC, limit, self.OFFSET_ZERO )

	def readTableItemTimeSkip(self, start, end, skip, limit):
		where_time = self.buildTimeWhere( start, end )
		row1 = self.selectOne( self.TABLE_ITEM, where_time, self.ORDER_ASC )
		if not row1:
			return []
		id_start = row1["id"]
		row2 = self.selectOne( self.TABLE_ITEM, where_time, self.ORDER_DESC )
		if not row2:
			return []
		id_end = row2["id"]
		id_list = range(id_start, (id_end + skip), skip)
		str_list = map(str, id_list)
		where_in = " WHERE id IN (" + ",".join(str_list) + ")"	
		return self.selectAll( self.TABLE_ITEM, where_in, self.ORDER_DESC, limit, self.OFFSET_ZERO )
		
	def readAllTableItemTime(self,  start, end, limit):	
		where = self.buildTimeWhere( start, end )
		return self.selectAll( self.TABLE_ITEM, where, self.ORDER_DESC, self.LIMIT_NONE, self.OFFSET_ZERO )

	def buildTimeWhere(self, start, end):
		text  = "WHERE ( time > "  + str(int(start))
		text += " AND time < " + str(int(end))
		text += " ) "
		return text

	def insertTableItem(self, time, module, temp, humi, pressure, light, noise):
		return self.insert( 
			self.TABLE_ITEM, 
			self.makeParamsTableItem( time, module, temp, humi, pressure, light, noise ) )

	def updateTableItem(self, id, time, module, temp, humi, pressure, light, noise):
		return self.update( 
			self.TABLE_ITEM, id, 
			self.makeParamsTableItem( time, module, temp, humi, pressure, light, noise ) )

	def updateTableItemNoise(self, id, noise):
		params = { "noise": float( noise )	}
		return self.update( self.TABLE_ITEM, id, params )

	def deleteTableItem(self, id):	
		return self.delete( self.TABLE_ITEM, id )

	def deleteAllTableItem(self):
		return self.truncateTable( self.TABLE_ITEM )

	def makeParamsTableItem(self, time, module, temp, humi, pressure, light, noise):		
		params = None
		try:	
			params = { \
				"time":int( time ), \
				"module": str( module ), \
				"temperature": float( temp ), \
				"humidity": float( humi ), \
				"pressure": float( pressure ), \
				"light": float( light ), \
				"noise": float( noise ) \
			}
		except:
			self.printExcept()			
		return params	

	def makeFormTableItem(self, time, module, temp, humi, pressure, light, noise):
		params = []
		params.append( ["time", int( time )] )
		params.append( ["module", str( module )] )
		params.append( ["temperature", float( temp )] )
		params.append( ["humidity", float( humi )] )
		params.append( ["pressure", float( pressure )] )
		params.append( ["light", float( light )] )
		params.append( ["noise", float( noise )] )							
		return params

# class end
