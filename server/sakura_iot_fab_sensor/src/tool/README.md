# tool - SAKURA IoT Platform Alpha

- init.sh <br/>
copy the following program to the system directory <br/>
- check_server.py <br/>
This program, to monitor the life-and-death of Sakura IoT Fab Sensor server. <br/>
It is normal, that the unixtime sent back from the server and the current time of this program matches. <br/>
If abnormal, this program restart the server and send the email. <br/>

- check_mysql_server.py <br/>
This program, to monitor the life-and-death of Mysql server. <br/>
It is normal, that  the number of records in the specified table is 0 or more <br/>
If abnormal, this program restart themysql server and send the email. <br/>

- check_server <br/>
for cron <br/>

- check_mysql_server <br/>
for cron <br/>

- mysql_base.py <br/>
basic library of mysql <br/>

- mysql_checker.py <br/>
monitor the life-and-death of Mysql server <br/>

- server_conf.py <br/>
handling setting flie of server <br/>
