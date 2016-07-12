#!/usr/bin/env python
# Sakura IoT Sensor
# 2016-07-01 K.OHWADA @ FabLab Kannai

from server import server_run
from sensor_util import SensorUtil
import argparse

# constant
APP_NAME = "sakura_iot_fab_sensor"
SERVER_HOST_DEFAULT = "0.0.0.0"
SERVER_PORT_DEFAULT = 5050

# main
def main():
    parser = argparse.ArgumentParser(prog="run")
    parser.add_argument("--host", action="store", type=str, dest="host",
        help="Specify the server hos")
    parser.add_argument("--port", action="store", type=int, dest="port",
        help="Specify the server port")  
    parser.add_argument("--basedir", action="store", type=str, dest="basedir",
        help="Specify the basedir to use for config. ")
    args = parser.parse_args()
    util = SensorUtil()
    host = util.initParam(args.host, SERVER_HOST_DEFAULT)
    port = util.initParam(args.port, SERVER_PORT_DEFAULT)
    basedir = util.initBasedir(args.basedir, APP_NAME)
    conf = util.initConfig( basedir )
    server_run( host, port, conf )

if __name__ == "__main__":
    main()
