# Specification of Sakura IoT Fab Sensor Server

### Overview
a web server written with python flask.
store sensor data  in databese
sensor data are collected via Sakura IoT

## function of Web Server
different processing depending on the path of url to access

### (1)  "/"　
display sensor data in line chart

specify the range of time of the data to be displayed with parameters.

? r = <renge type> & s = <date time of start> & e = <date time of end>

<renge type>
day: Last 1 day (when parameter is omitted)
week: Last week
month: Last January
year: Last 1 year
period: specify the period with 
<date time of start> and <date time of end>
date time is a string like yyyy - MM - dd hh: mm

### (2)  "/api"

return The sensor data of the most recent one day  in the json format

### (3)  "/post”

at POST method, store sensor data  in the database.
It corresponds to outgoing of Sakura IoT Platform.
Check the validity by X - Sakura - Signature of the header part.
Sensor data is in json format

### (4)'/status'
return the status of the server.
for monitoring life-and-death of server
If it is normal, return the unix time of the current time

### (5) '/login'

 login processing
at GET method, display a form of a user name and a password for login.
at POST method, if the user name and the password value match the value of the setting file, the login state is set


### (6) '/logout'

 logout processing
at POST method, cancel login state

### (7) ”/manage”

manage  the sensor data in the database.
If not in the login state, move login
at GET method, display a form for add new , update and delete.
at POST method, performe add new, update, and delete

## Manage of web server
monitor life-and-death of server
if  abnormal, restart server.






