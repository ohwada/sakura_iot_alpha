# Server - SAKURA IoT Platform Alpha

## sakura_iot_fab_sensor
Web app display sensor data in line chart<br/>
Receive data from Sakura IoT Platform. <br/>
Store data in MySQL database. <br/> 
Read data from the database, and display in [Google Chart]
(https://developers.google.com/chart/interactive/docs/gallery/linechart). <br/>

[Arduino sketch](https://github.com/ohwada/sakura_iot_alpha/tree/master/arduino/sakura_iot_fab_sensor) in sensor side <br/>

<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_fab_sensor_system.png" width="500" />

### Requirements <br/>
- OS: Linux ( recommend Debian ) <br/>
- MySQL<br/>
- Python 2.7 <br/>
- [python-dev](https://packages.debian.org/jessie/python-dev) <br/>
- [Virtualenv](https://virtualenv.readthedocs.org/en/latest/) <br/>

### Install
$ cd ~<br>
$ mkdir virtualenv<br>
Copy directory sakura_iot_fab_sensor under directory /home/YOUR_USER/virtualenv <br/>

> cd ~/virtualenv <br/>
> $ virtualenv venv <br/>
( You do not need to excute this command more than once, if you excuted this at once. ) <br/>

> $ source venv/bin/activate <br/>
(venv) $ cd sakura_iot_fab_sensor <br/>
(venv) $ python setup.py install <br/>
(venv) $ deactivate <br/>

you can use service daemon for Debian <br/>
> $ sudo sh init.sh <br/>
edit script file  <br>
$ vi /etc/default/sakura-iot-fab-sensor <br>

run at once <br>
 pip install --upgrade MySQL-python
$ pip install --upgrade flask
$ cd ~/virtualenv/sakura_iot_fab_sensor<br>
$ run python run.py <br>

edit setting file  <br>
$ cd ~/.sakura_iot_fab_sensor/conf<br>
$ vi user.conf <br>

### run service daemon <br>
> $ sudo /etc/init.d/sakura-iot-fab-sensor start <br/>

### quite service daemon <br>
> $ sudo insserv -r sakura-iot-fab-sensor

### Usage
Access using web browser. <br/>
http://YOUR_SERVER_URL:5050/ <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/graph_whole.png" width="300" />
- route none <br/>
display sensor data in graph <br/>
- route api <br/>
return one day sensor data <br/>
- route post <br/>
store sensor data to database<br/>
- route status <br/>
return unixtime when server status is green

### Blog (Japanese)
http://android.ohwada.jp/archives/7077
