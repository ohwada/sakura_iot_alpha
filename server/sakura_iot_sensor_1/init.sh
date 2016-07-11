#!/bin/sh
# sakura-iot-sensor-1
# 2016-07-01 K.OHWADA @ FabLab Kannai

cp scripts/sakura-iot-sensor-1.init /etc/init.d/sakura-iot-sensor-1
chmod 755 /etc/init.d/sakura-iot-sensor-1
cp scripts/sakura-iot-sensor-1.default /etc/default/sakura-iot-sensor-1
chmod 644 /etc/default/sakura-iot-sensor-1
insserv sakura-iot-sensor-1
systemctl daemon-reload
