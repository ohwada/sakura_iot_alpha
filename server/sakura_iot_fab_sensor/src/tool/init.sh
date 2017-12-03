#!/bin/sh
# sakura-iot-fab-sensor
# 2017-11-01 K.OHWADA 

mkdir /root/bin
cp *.py /root/bin
cp  check_mysql_server /etc/cron.hourly
cp  check_sakura-iot_server /etc/cron.hourly
pip install --upgrade MySQL-python
pip install --upgrade email
