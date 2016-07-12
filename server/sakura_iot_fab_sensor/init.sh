#!/bin/sh
# sakura-iot-fab-sensor
# 2016-07-01 K.OHWADA @ FabLab Kannai

cp scripts/sakura-iot-fab-sensor.init /etc/init.d/sakura-iot-fab-sensor
chmod 755 /etc/init.d/sakura-iot-fab-sensor
cp scripts/sakura-iot-fab-sensor.default /etc/default/sakura-iot-fab-sensor
chmod 644 /etc/default/sakura-iot-fab-sensor
insserv sakura-iot-fab-sensor
systemctl daemon-reload
