#!/usr/bin/env python
# sakura_iot_sensor_1
# 2016-05-01 K.OHWADA @ FabLab Kannai

import os
import sys

basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(basedir, "src"))

import sakura_iot_sensor_1
sakura_iot_sensor_1.main()
