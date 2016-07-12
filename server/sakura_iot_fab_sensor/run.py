#!/usr/bin/env python
# sakura_iot_fab_sensor
# 2016-07-01 K.OHWADA

import os
import sys

basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(basedir, "src"))

import sakura_iot_fab_sensor
sakura_iot_fab_sensor.main()
