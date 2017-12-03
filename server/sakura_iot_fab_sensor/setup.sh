#!/bin/sh
# sakura-iot-fab-sensor 
# setup for Debian
# run as root
# 2017-11-01 K.OHWADA

sudo apt-get install --upgrade libmysqlclient-dev
apt-get  install --upgrade mysql-server
apt-get install --upgrade python2.7
apt-get install --upgrade python-dev
apt-get install --upgrade virtualenv
pip install --upgrade pip
