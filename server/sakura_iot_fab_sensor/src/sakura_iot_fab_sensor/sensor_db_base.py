# SensorDbBase
# 2016-07-01 K.OHWDA

import MySQLdb
import sys
import traceback

# SensorDbBase
class SensorDbBase():
			
	DB_HOST = "localhost"
	DB_CHARSET = "utf8"
	DEBUG = True

	LF = "\n"
	OFFSET_ZERO = 0
	LIMIT_ONE = 1
	DEBUG = True

	logger = None
	conn = None

	def setLogger(self, logger):
		self.logger = logger

	def connectParam(self, param):
		return self.connect( param["db_name"], param["user"], param["passwd"] )
			
	def connect(self, db_name, user, passwd):
		ret = False
		try:
			self.conn = MySQLdb.connect( host=self.DB_HOST, db=db_name, user=user, passwd=passwd, charset=self.DB_CHARSET )
			ret = True
		except:
			self.printExcept()
		return ret

	def close(self):
		self.conn.close()
		self.conn = None

	def existsTable(self, name):
		tables = self.showTables()
		if tables is None: return False	
		for table in tables:
			if table == name: return True
		return False	

	def showTables(self):
		sql = "SHOW TABLES"
		result = self.getResultList( sql )
		if result is None: return None
		rows = []
		for row in result:
    			rows.append( row[0] )
		return rows

	def truncateTable(self, table):
		sql = "TRUNCATE " + table
		return self.execute(sql)

	def selectCount(self, table, where):
		sql = "SELECT count(*) FROM " + table + " " + where
		return self.getResultCount( sql )

	def selectOneById(self, table, id):
		rows = self.selectById(table, id)
		if not rows:
			return None
		return rows[0]

	def selectById(self, table, id):
		sql = "SELECT * FROM " + table + " WHERE id=" + str(int(id))
		return self.getResultDict( sql )

	def selectAll(self, table, where, order, limit, offset):
		sql = "SELECT * FROM " + table + " " + where + " ORDER BY id " + order
		if limit > 0:
			sql += " LIMIT " + str(int(limit))
			if offset > 0:
				sql += " OFFSET " + str(int(offset))
		return self.getResultDict( sql )

	def selectOne(self, table, where, order):
		rows = self.selectAll( table, where, order, self.LIMIT_ONE, self.OFFSET_ZERO )
		if not rows:
			return None
		return rows[0]

	def insert(self, table, params):
		ret = False
		if params is None: return ret
		try:
			keys = []
			values = []
			for k, v in params.items():
				keys.append( str(k) )
				values.append( self.escape( v ))
			str_key = ", ".join(keys)
			str_value = ", ".join(values)
			sql = "INSERT INTO " + table + " (" + str_key + ") VALUES (" + str_value  + ")"
			if self.DEBUG: print sql
			ret = self.execute( sql )
		except:
			self.printExcept()		
		return ret

	def update(self, table, id, params):
		ret = False
		if params is None: return ret
		try:
			sets = []
			for k, v in params.items():
				sets.append( str(k) + "=" + self.escape( v ) )
			str_set = ", ".join(sets)
			sql = "UPDATE " + table + " SET " + str_set + " WHERE id=" + str(int(id))
			ret = self.execute( sql )
		except:
			self.printExcept()		
		return ret

	def delete(self, table, id):
		sql = "DELETE FROM " + table + " WHERE id=" + str(int(id))
		return self.execute( sql )

	def escape(self, v):
		text = "'" + MySQLdb.escape_string( str(v) ) + "'"
		return text

	def execute(self, sql):
		ret = False
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			self.conn.commit()      
			cursor.close()
			ret = True
		except:
			self.printExcept()
		return ret

	def getResultCount(self, sql):
		ret = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			result = cursor.fetchone()
			cursor.close()
			ret = int( result[0] )
		except:
			self.printExcept()
		return ret
		
	def getResultList(self, sql):
		result = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			result = cursor.fetchall()
			cursor.close()
		except:
			self.printExcept()
		return result

	def getResultDict(self, sql):
		result = None
		try:
			cursor = self.conn.cursor( MySQLdb.cursors.DictCursor )
			cursor.execute(sql)
			result = cursor.fetchall()
			cursor.close()
		except:
			self.printExcept()
		return result

	def printResultList(self, result):
		for row in result:
			for i in range(0, len(row)):
				print row[i] + ", ",
			print ""

	def printResultDict(self, result):
		for row in result:
			for k, v in row.items():
				print str(k) + ":" + str(v) + ", ",
			print ""

	def printExcept(self):
		info = sys.exc_info()
		msg = "DB Error:" + self.LF
		msg += str(info[0]) + self.LF
		msg += str(info[1]) + self.LF
		tbinfo = traceback.format_tb( info[2] )
		for tb in tbinfo:
			msg += tb + self.LF
		if self.logger:
			self.logger.error(msg)
		print msg
		            			
# class end
