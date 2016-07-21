# SensorPost
# 2016-07-01 K.OHWDA

from sensor_db import SensorDb
from sensor_util import SensorUtil
from pprint import pprint
import json

# data format from Sakura IoT Platform
# {"module": "unfam4F5msY5", "datetime": "2016-07-06T22:13:34.291162188Z", "payload": {"channels": [{"value": 29, "channel": 0, "type": "f"}, {"value": 49, "channel": 1, "type": "f"}, {"value": 1005.4416, "channel": 2, "type": "f"}, {"value": 52.26, "channel": 3, "type": "f"}, {"value": 15.969971, "channel": 4, "type": "f"}]}, "type": "channels"}

# channel assignment
# ch0: temperature
# ch1: humidity
# ch2: pressure
# ch3: light
# ch4: noise

# SensorPost
class SensorPost():

	app = None
	db = None
	util = None
	
	def __init__(self, app, db):
		self.app = app
		self.db = db
		self.util = SensorUtil()

	def excute(self, data):
		if not data: 
			error = "param error: no data"
			print error
			self.app.logger.error( error )	
			return
		obj = json.loads( data )
		if (obj["type"] is None) or (obj["type"] != "channels"):
			error = "param error: " + str(data)
			print error
			self.app.logger.error( error )	
			return
		# type is "channels"
		self.app.logger.debug( data )
		self.parseChannels( obj )

	def parseChannels(self, obj):
		unixtime = self.util.convUnixtime( obj["datetime"] )
		module = str(obj["module"])
		channels = obj["payload"]["channels"]
		new_chs = [0, 0, 0, 0, 0]
		# rearrange in numerical order of channnel
		# because the order is falling apart
		for ch in channels:
			ch_type = str(ch["type"])
			ch_num = int(ch["channel"])
			if (ch_type == 'f') and (ch_num >= 0) and (ch_num <= 4):				
				# rearrange, if expect format
				new_chs[ ch_num ] = float( ch["value"] )
			else:	
				# if otherwise
				error = "param error: " + pprint.pformat( ch )
				print error
				self.app.logger.error( error )	
		# save to database		
		self.db.insertTableItem( unixtime, module, new_chs[0], new_chs[1], new_chs[2], new_chs[3], new_chs[4] )
				
# class end
