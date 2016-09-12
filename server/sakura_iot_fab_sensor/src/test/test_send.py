#!/usr/bin/env python

# test send
# 2016-09-01 K.OHWADA

'''
test for @app.route('/post')
This program, to send data of Sakura IoT Fab Sensor server.
'''

from sakura_iot_send import SakuraIotSend
import time
import random

# === main ===            
URL = "http://localhost:5050/post"
SECRET = "your_secrect"
MODULE = "abc"

CH_TYPE = "f"        

GEN_MINS = [10,  30, 950, 100, 400]
GEN_MAXS = [30, 80, 1050, 300, 600]
gan_values = [0, 0, 0, 0, 0]
gen_divs = [20, 50, 1000, 200, 500]

def genValues(self):
	# make five values
	for i in range(0, 5):
		v = gen_values[i]
		v += gen_divs[i]
		if v < GEN_MINS[i]:					
			# invert div, when smaller
			v = GEN_MINS[i]
			gen_divs[i] = random.uniform(0.05, 1.0)
		elif v > GEN_MAXS[i]:
			# invert div, when bigger
			v = GEN_MAXS[i]
			gen_divs[i] = - random.uniform(0.05, 1.0)
		gen_values[i] = v

iot = SakuraIotSend()
iot.setUrl(URL)
iot.setSecret(SECRET)
iot.setModule(MODULE)
       
while True:
    value_array = genValus( value_array )
    channels = []
    for ch in range(0, 5):
        channels.append( iot.buildChannel( ch, CH_TYPE, value_array[ch]) )
    data = iot.buildJsonChannels( channels )
    print data
    res = iot.send(data)
    time.sleep(1)
