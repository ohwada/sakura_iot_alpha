#!/usr/bin/env python

# fab_sensor_line_chart.py
# display Temperature on line chart
# get data from the server

import urllib
import json
from matplotlib import pyplot
import matplotlib.dates as mdates
import datetime
import time

URL = "your server"

FILE_PATH = "test.json"

# date time
TIME_ZONE = 9 # JST (UTC+9)
DATE_FORMAT = "%Y-%m-%d %H:%M"
DATE_FORMAT_MINUTE = "%H:%M"
DATE_FORMAT_X_AXIS = "%m-%d %H:%M"
# 1 hour = 3600 sec
PERIOD_SEC = 36000
#
# read file
#
def read(file_path):
    text = open( file_path ).read()
    return text
#-----   
   
#
# http get
# 
def get( url ):
    result = urllib.urlopen( url ).read()
    return result
#-----

#
# parse json
# 
def parse( json_text ):
    obj = json.loads( json_text )
    items = obj["items"]
    num = obj["num"]

    time_arr = []
    temperature_arr = []
    humidity_arr = []
       
    for item in items:
        time_arr.append( item["time"] )
        temperature_arr.append( item["temperature"] )
        humidity_arr.append( item["humidity"] ) 
#-----  

    return [ num,  time_arr, temperature_arr,  humidity_arr]
#-----  


 #
# convDateTime
# 
def convDateTime( time_arr ):
    dt_arr = []	
    for t in time_arr:
        dt = datetime.datetime.fromtimestamp( t )
        dt_arr.append( dt ) 
#-----  
    return dt_arr
#----- 



 #
# convElapseTime
# 
def convElapseTime( time_arr ):
    elapse_arr = []	
    start = time_arr[0]
    for t in time_arr:
        elapse = ( t - start ) / PERIOD_SEC
        elapse_arr.append( elapse ) 
#-----  
    return elapse_arr
#-----  

 #
# convFormatTime
# 
def convFormatTime( time_arr ):
    format_arr = []	
    for t in time_arr:
        f = getFormatTime( t, DATE_FORMAT_MINUTE )
        format_arr.append( f ) 
#-----  
    return format_arr
#-----  

 #
# getFormatTime
# 
def getFormatTime(unixtime, format ):	    
    dt = datetime.datetime.fromtimestamp( unixtime )
    # UTC -> Local
    local = dt + datetime.timedelta( hours=TIME_ZONE )
    return local.strftime( format )
#-----  		

		
#
# === main ===
#
# text = read( FILE_PATH ) 
text = get( URL )
ret = parse( text )
#print ret[0]
#print ret[2]
num=ret[0]
num1=num -1
time_arr = ret[1]
print "num: " + str(num)
print "start: " + getFormatTime( time_arr[0],  DATE_FORMAT )
print "end: " + getFormatTime( time_arr[num1],  DATE_FORMAT )
 
# 71690  > 1000
div_num = ( time_arr[num1] - time_arr[0] ) / 60
print div_num
 
# line chart  
x = convDateTime( ret[1] )
#print len(x)

y = ret[2]
#print len(y)

fig = pyplot.figure()
ax = fig.add_subplot( 111, title='Temperature', xlabel='datetime' )
ax.plot(x, y)

# x axies

#ax.xaxis.set_major_locator( mdates.DayLocator() )
ax.xaxis.set_major_locator( mdates.HourLocator() )

daysFmt = mdates.DateFormatter( DATE_FORMAT_X_AXIS )
ax.xaxis.set_major_formatter(daysFmt)
fig.autofmt_xdate( rotation=90 )

pyplot.show()
#-----