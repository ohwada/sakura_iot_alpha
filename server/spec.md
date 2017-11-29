# Specification of Sakura IoT Fab Sensor Server

### Overview <br/>
a web server written with python flask.
store sensor data  in databese
sensor data are collected via Sakura IoT

## function of Web Server <br/>
different processing depending on the path of url to access

### (1)  "/"　
display sensor data in line chart <br/>

specify the range of time of the data to be displayed with parameters. <br/>

? r = &lt;renge type&gt; & s = &lt;date time of start&gt; &amp; e = &lt;date time of end&gt; <br/>

<renge type>
day: Last one day (when parameter is omitted) <br/>
week: Last one week <br/>
month: Last one month <br/>
year: Last one year <br/>
period: specify the period with 
date time of start and date time of end <br/>
date time is a string like yyyy - MM - dd hh: mm <br/>

<img src="https://raw.githubusercontent.com/ohwada/sakura_iot_alpha/master/server/docs/sakura_iot_fab_sensor_main.png" width="300"/> <br/>

### (2)  "/api" <br/>
return The sensor data of the most recent one day  in the json format <br/>

### (3)  "/post” <br/>

at POST method, store sensor data  in the database. <br/>
corresponds to outgoing of Sakura IoT Platform. <br/>
Check the validity by X - Sakura - Signature of the header part. <br/>
data format from Sakura IoT Platform<br/>
 json format <br/>
 {"module": "unfam4F5msY5", "datetime": "2016-07-06T22:13:34.291162188Z", "payload": {"channels": [{"value": 29, "channel": 0, "type": "f"}, {"value": 49, "channel": 1, "type": "f"}, {"value": 1005.4416, "channel": 2, "type": "f"}, {"value": 52.26, "channel": 3, "type": "f"}, {"value": 15.969971, "channel": 4, "type": "f"}]}, "type": "channels"}

channel assignment<br/>
 - ch0: temperature<br/>
 - ch1: humidity<br/>
 - ch2: pressure<br/>
 - ch3: light<br/>
 - ch4: noise<br/>
 
### (4)'/status' <br/>
return the status of the server. <br/>
for monitoring life-and-death of server <br/>
If it is normal, return the unix time of the current time <br/>

### (5) '/login' <br/>

 login processing <br/>
at GET method, display a form of a user name and a password for login. <br/>
at POST method, if the user name and the password value match the value of the setting file, set the login state  <br/>

<img src="https://raw.githubusercontent.com/ohwada/sakura_iot_alpha/master/server/docs/sakura_iot_fab_sensor_login.png" width="300"/> <br/>

### (6) '/logout' <br/>

 logout processing <br/>
at POST method, cancel login state <br/>

### (7) ”/manage” <br/>

manage  the sensor data in the database. <br/>
If not in the login state, move login <br/>
at GET method, display a form for add new , update and delete. <br/>
at POST method, performe to add new, update, and delete <br/>

<img src="https://raw.githubusercontent.com/ohwada/sakura_iot_alpha/master/server/docs/sakura_iot_fab_sensor_manage.png" width="300"/> <br/>

### setting file  <br/>

 file path : <br/>
Home directory / 2016 .sakura_iot_fab_sensor/conf/user.conf

 contents  : <br/>
Login user name and password, <br/>
Database user name and password. etc <br/>

## Manage of web server <br/>
monitor life-and-death of server <br/>
if  abnormal, restart server. <br/>






