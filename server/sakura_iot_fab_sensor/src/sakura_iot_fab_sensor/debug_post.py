# debug post
# 2016-07-01 K.OHWDA

import urllib2
import json

URL = 'http://localhost:5050/post'
param = {"type": "channels", "payload": {"channels": [{"channel": 0, "value": 31, "type": "f"}, {"channel": 1, "value": 43, "type": "f"}, {"channel": 2, "value": 1006.2096, "type": "f"}, {"channel": 3, "value": 0, "type": "f"}, {"channel": 4, "value": 4.5300293, "type": "f"}]}, "datetime": "2016-07-01T14:45:07.467808166Z", "module": "abc"}

data = json.dumps( param )
req = urllib2.Request( URL, data, {'Content-Type': 'application/json'} )
response = urllib2.urlopen( req )
print response.read()
