# SensorPost
# 2016-07-01 K.OHWDA

from sensor_db import SensorDb
from sensor_util import SensorUtil
from pprint import pprint
import json

# data format
# {"module": "unfam4F5msY5", "datetime": "2016-07-06T22:13:34.291162188Z", "payload": {"channels": [{"value": 29, "channel": 0, "type": "f"}, {"value": 49, "channel": 1, "type": "f"}, {"value": 1005.4416, "channel": 2, "type": "f"}, {"value": 52.26, "channel": 3, "type": "f"}, {"value": 15.969971, "channel": 4, "type": "f"}]}, "type": "channels"}

# SensorPost
class SensorPost():

	db = None
	util = None
	
	def __init__(self, db):
		self.db = db
		self.util = SensorUtil()

	def excute(self, data):
		if not data: 
			print "param error: no data"
			return;
		obj = json.loads(data)
		if obj["type"] is None:
			print "param error: " + str(data)
			return
		str_type = obj["type"] 
		if str_type == "keepalive":
			print str(data)
			return
		elif str_type == "channels":  
			self.parseChannels(obj)                          

	def parseChannels(self, obj):
		unixtime = self.util.convUnixtime( obj["datetime"] )
		module = str(obj["module"])
		channels = obj["payload"]["channels"]
		new_chs = [0, 0, 0, 0, 0]
		for ch in channels:
			ch_type = str(ch["type"])
			ch_num = int(ch["channel"])
			if (ch_type == 'f') and (ch_num >= 0) and (ch_num <= 4):
				new_chs[ ch_num ] = float( ch["value"] )
			else:
				print "param error: ",
				pprint(ch)
		self.db.insertTableItem( unixtime, module, new_chs[0], new_chs[1], new_chs[2], new_chs[3], new_chs[4] )

# class end
