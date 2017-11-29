# SensorPost
# 2016-07-01 K.OHWDA

""" post

at POST method, store sensor data  in the database.
It corresponds to outgoing of Sakura Iot Platform.
Check the validity by X - Sakura - Signature of the header part.
Sensor data is in json format

data format from Sakura IoT Platform
 {"module": "unfam4F5msY5", "datetime": "2016-07-06T22:13:34.291162188Z", "payload": {"channels": [{"value": 29, "channel": 0, "type": "f"}, {"value": 49, "channel": 1, "type": "f"}, {"value": 1005.4416, "channel": 2, "type": "f"}, {"value": 52.26, "channel": 3, "type": "f"}, {"value": 15.969971, "channel": 4, "type": "f"}]}, "type": "channels"}

channel assignment
 ch0: temperature
 ch1: humidity
 ch2: pressure
 ch3: light
 ch4: noise
 
"""

from sensor_db import SensorDb
from sensor_util import SensorUtil
import json
import dateutil.parser
import time
import sys
import traceback
import hmac
import hashlib

# SensorPost
class SensorPost():

	LF = "\n"

	db = None
	db_param = None
	logger = None
	util = None
	secret = None

	def __init__(self, db_param, logger, secret):
		self.db_param = db_param
		self.logger = logger
		self.secret = secret
		self.util = SensorUtil()

	def excute(self, signature, data):
		self.db = SensorDb()
		self.db.setLogger( self.logger )
		ret = self.db.connectParam( self.db_param )
		if ret:
			# connect to DB
			self.post(signature, data)
			self.db.close()
				
	def post(self, signature, data):
		try:
			calc_signature = hmac.new( self.secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha1 ).hexdigest()
			self.logger.debug( signature )
			self.logger.debug( data )
			print data
			if signature == calc_signature:
				obj = json.loads( data )
				if obj["type"] == "channels":
					self.parseChannels( obj )
			else:
				msg = "signature unmatch" + self.LF
				msg += signature + self.LF
				msg += calc_signature
				print msg
				self.logger.debug( msg )
		except:
			self.printExcept()		

	def parseChannels(self, obj):
		try:
			dt = dateutil.parser.parse( obj["datetime"] )
			unixtime = int(time.mktime( dt.timetuple() ))
			module = str(obj["module"])
			chs = self.parsePayloadChannels( obj["payload"]["channels"] )
			# save to database
			if chs:		
				self.db.insertTableItem( unixtime, module, chs[0], chs[1], chs[2], chs[3], chs[4] )
		except:
			self.printExcept()		

	def parsePayloadChannels(self, channels):
		new_chs = [0, 0, 0, 0, 0]
		try:
			# rearrange in numerical order of channnel
			# because the order is falling apart
			for ch in channels:
				ch_type = str(ch["type"])
				ch_num = int(ch["channel"])
				if (ch_type == 'f') and (ch_num >= 0) and (ch_num <= 4):				
					# rearrange, if expect format
					new_chs[ ch_num ] = float( ch["value"] )
		except:
			new_chs = None
			self.printExcept()		
		return new_chs

	def printExcept(self):
		info = sys.exc_info()
		msg = "Post Error:" + self.LF
		msg += str(info[0]) + self.LF
		msg += str(info[1]) + self.LF
		tbinfo = traceback.format_tb( info[2] )
		for tb in tbinfo:
			msg += tb + self.LF
		self.logger.error(msg)
		print msg
			
# class end
