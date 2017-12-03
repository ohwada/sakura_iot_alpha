# Mysql
# 2016-07-01 K.OHWDA

import MySQLdb
import sys
import traceback

# MysqlBase
class MysqlBase():
			
	LF = "\n"
	OFFSET_ZERO = 0
	LIMIT_ONE = 1
	DEBUG = True

	logger = None
	conn = None

# setLogger
	def setLogger(self, logger):
		self.logger = logger
# ---

# onnectParam
	def connectParam(self, param):
		return self.connect( param["db_name"], param["user"], param["passwd"] )
# ---

# 	connect
	def connect(self, db_name, user, passwd):
		con_user = str(user)
		con_passwd =  str(passwd)
		con_db = str(db_name)
		print con_user
		print con_passwd
		print con_db
		ret = False
		try:
			self.conn = MySQLdb.connect( user=con_user,  passwd=con_passwd, db=con_db )
			ret = True
		except:
			self.printExcept()
		return ret
# ---

# close
	def close(self):
		self.conn.close()
		self.conn = None

	def existsTable(self, name):
		tables = self.showTables()
		if tables is None: return False	
		for table in tables:
			if table == name: return True
		return False	
# ---

#  showTables
	def showTables(self):
		sql = "SHOW TABLES"
		result = self.getResultList( sql )
		if result is None: return None
		rows = []
		for row in result:
    			rows.append( row[0] )
		return rows
# ---

# truncateTable
	def truncateTable(self, table):
		sql = "TRUNCATE " + table
		return self.execute(sql)
# ---

# selectCount
	def selectCount(self, table, where):
		sql = "SELECT count(*) FROM " + table + " " + where
		return self.getResultCount( sql )
# ---

# selectOneById
	def selectOneById(self, table, id):
		rows = self.selectById(table, id)
		if not rows:
			return None
		return rows[0]
# ---

# selectById
	def selectById(self, table, id):
		sql = "SELECT * FROM " + table + " WHERE id=" + str(int(id))
		return self.getResultDict( sql )
# ---

# electAll
	def selectAll(self, table, where, order, limit, offset):
#		sql = "SELECT * FROM " + table + " " + where + " ORDER BY id " + order
		sql = "SELECT * FROM " + table + " " + where + " ORDER BY " + order
		if limit > 0:
			sql += " LIMIT " + str(int(limit))
			if offset > 0:
				sql += " OFFSET " + str(int(offset))
		return self.getResultDict( sql )
# ---

# selectOne
	def selectOne(self, table, where, order):
		rows = self.selectAll( table, where, order, self.LIMIT_ONE, self.OFFSET_ZERO )
		if not rows:
			return None
		return rows[0]
# ---

#  insert
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
# ---

# update
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
# ---

# delete
	def delete(self, table, id):
		sql = "DELETE FROM " + table + " WHERE id=" + str(int(id))
		return self.execute( sql )
# ---

# escape
	def escape(self, v):
		text = "'" + MySQLdb.escape_string( str(v) ) + "'"
		return text
# ---

# execute
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
# ---

# getResultCount
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
# ---

# 	getResultList	
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
# ---

# getResultDict
	def getResultDict(self, sql):
		# print sql
		result = None
		try:
			cursor = self.conn.cursor( MySQLdb.cursors.DictCursor )
			cursor.execute(sql)
			result = cursor.fetchall()
			cursor.close()
		except:
			self.printExcept()
		return result
# ---

# printResultList
	def printResultList(self, result):
		for row in result:
			for i in range(0, len(row)):
				print row[i] + ", ",
			print ""
# ---

# printResultDict
	def printResultDict(self, result):
		for row in result:
			for k, v in row.items():
				print str(k) + ":" + str(v) + ", ",
			print ""
# ---

# printExcept
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
# ---
		            			
# class end
