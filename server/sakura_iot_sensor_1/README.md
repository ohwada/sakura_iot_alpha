# Server - SAKURA IoT Platform Alpha

## sakura_iot_sensor_1
Web app display sensor data in graph <br/>

Receive data from Sakura IoT Platform. <br/>
Store data in MySQL database. <br/> 
Read data from the database, and display in (Google Chart)[https://developers.google.com/chart/interactive/docs/gallery/linechart]. <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_sensor_1_system.png" width="300" />

### Requirements
- OS: Linux <br/>
- Python 2.7 <br/>
- [python-dev](https://packages.debian.org/jessie/python-dev) <br/>
- [Virtualenv](https://virtualenv.readthedocs.org/en/latest/) <br/>

### Install
Copy directory sakura_iot_sensor_1 under directory /home/YOUR_USER/virtualenv

> cd ~/virtualenv
> $ virtualenv venv <br/>
( You do not need to excute this command more than once, if you excuted this at once. ) <br/>

> $ source venv/bin/activate <br/>
(venv) $ cd  sakura_iot_sensor_1<br/>
(venv) $ python setup.py install <br/>
(venv) $ deactivate <br/>

you can use service daemon <br/>
> $ sudo sh init.sh <br/>

### Run
> $ cd ~<br/>
$ sudo virtualenv/venv/bin/sakura_iot_sensor_1 <br/>

or service daemon <br/>
> $ sudo /etc/init.d/sakura_iot_sensor_1 start <br/>

### Quite service daemon
> $ sudo insserv -r sakura_iot_sensor_1

### Usage
Access using web browser. <br/>
http://YOUR_SERVER_URL:5050/ <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/graph_whole.png" width="200" />

### Blog (Japanese)
http://android.ohwada.jp/archives/7077
