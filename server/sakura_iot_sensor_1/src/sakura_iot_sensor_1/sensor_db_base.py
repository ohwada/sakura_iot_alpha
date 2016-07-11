# SensorDbBase
# 2016-07-01 K.OHWDA

import MySQLdb

# SensorDbBase
class SensorDbBase():
	DB_HOST = "localhost"
	DB_CHARSET = "utf8"
	DEBUG = True

	OFFSET_ZERO = 0
	LIMIT_ONE = 1
	
	conn = None
	sql = ''
    	errors = []
	mysql_errors = []

	def connect(self, db, user, passwd):
		try:
			self.conn = MySQLdb.connect( host=self.DB_HOST, db=db, user=user, passwd=passwd, charset=self.DB_CHARSET )
		except MySQLdb.OperationalError as e:
			print e
		if self.conn is None: 
			self.addError( "mysql connect failed" )
			self.addMysqlError()
			return False
		return True

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
		keys = []
		values = []
		for k, v in params.items():
			keys.append( str(k) )
			values.append( self.escape( v ))
		str_key = ", ".join(keys)
		str_value = ", ".join(values)
		sql = "INSERT INTO " + table + " (" + str_key + ") VALUES (" + str_value  + ")"
		print sql
		return self.execute( sql )

	def update(self, table, id, params):
		sets = []
		for k, v in params.items():
			sets.append( str(k) + "=" + self.escape( v ) )
		str_set = ", ".join(sets)
		sql = "UPDATE " + table + " SET " + str_set + " WHERE id=" + str(int(id))
		return self.execute( sql )

	def delete(self, table, id):
		sql = "DELETE FROM " + table + " WHERE id=" + str(int(id))
		return self.execute( sql )

	def escape(self, v):
		text = "'" + MySQLdb.escape_string( str(v) ) + "'"
		return text

	def execute(self, sql):
		self.clearMysqlError()
		self.clearError()
		cursor = self.conn.cursor()      
		ret = self.executeCursor(cursor, sql)
		self.conn.commit()      
		cursor.close()
		if not ret:
			self. setExecuteError(sql)
		return ret

	def getResultCount(self, sql):
		self.clearMysqlError()
		self.clearError()
		cursor = self.conn.cursor()
		ret = self.executeCursor(cursor, sql)
		result = None
		if ret:
			result = self.fetchonelCursor(cursor)
		cursor.close()
		if result is None:
			self. setExecuteError(sql)
		return result[0]
		
	def getResultList(self, sql):
		self.clearMysqlError()
		self.clearError()
		cursor = self.conn.cursor()
		return self.getResultCommon( cursor, sql )

	def getResultDict(self, sql):
		self.clearMysqlError()
		self.clearError()
		cursor = self.conn.cursor( MySQLdb.cursors.DictCursor )
		return self.getResultCommon( cursor, sql )

	def getResultCommon(self, cursor, sql):
		ret = self.executeCursor(cursor, sql)
		result = None
		if ret:
			result = self.fetchallCursor(cursor)	
		cursor.close()
		if result is None:
			self. setExecuteError(sql)
		return result

	def executeCursor(self, cursor, sql):
		ret = False
		try:
			cursor.execute(sql)
			ret = True
		except MySQLdb.Error, e:
			try:
        			self.setMysqlError( "[%d]: %s" % (e.args[0], e.args[1]) )
    			except IndexError:
        			self.setMysqlError( str(e) )
        	return ret

	def fetchonelCursor(self, cursor):
		result = None
		try:
			result = cursor.fetchone()
		except MySQLdb.Error, e:
			try:
        			self.setMysqlError( "[%d]: %s" % (e.args[0], e.args[1]) )
    			except IndexError:
        			self.setMysqlError( str(e) )	
		return result

	def fetchallCursor(self, cursor):
		result = None
		try:
			result = cursor.fetchall()
		except MySQLdb.Error, e:
			try:
        			self.setMysqlError( "[%d]: %s" % (e.args[0], e.args[1]) )
    			except IndexError:
        			self.setMysqlError( str(e) )	
		return result
        			
	def setExecuteError(self, sql):
    		self.addError( sql )
    		self.addMysqlError()
    		if self.DEBUG:
    			print self.getError()

	def clearMysqlError(self):
		self.mysql_errors = []

	def setMysqlError(self, err):
		self.mysql_errors.append( err )

	def addMysqlError(self):
		if len(self.mysql_errors) == 0: return
		for err in self.mysql_errors:
			self.addError( "MySQL: " + err )

	def clearError(self):
		self.errors = []

	def addError(self, error):    
		self.errors.append( error )

	def getError(self, glue="\n"):
		if len( self.errors ) == 0: return ""
		return glue.join( self.errors )

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
			
# class end
