# Arduino - SAKURA IoT Platform Alpha

## sakura iot fab sensor
Send data obtained from sensors to Sakura IoT Platform <br/>

[Server side program](https://github.com/ohwada/sakura_iot_alpha/tree/master/server/sakura_iot_fab_sensor) <br/>

<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_fab_sensor_system.png" width="500" />

### Hardware
[Arduino Sensor Shield](https://github.com/FabLabKannai/sensor) <br/>
- Temperature and humidity : DHT11<br/>
- Air Pressure : MPL115A2<br/>
- Light : NJL7502L<br/>
- Noise : Condenser Microphone C9267<br/>

<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/fab_sensor_board.png" width="200" />

Sakura IoT comm board <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_soracom.png" width="200" />

### Software
Require library <br/>
- [Arduino Library for the DHT11](https://github.com/adafruit/DHT-sensor-library)
- [Driver for the Adafruit MPL115A2 barometric pressure sensor breakout](https://github.com/adafruit/Adafruit_MPL115A2)
- [SAKURA Internet IoT Alpha Communication Module Library for Arduino](https://github.com/sakura-internet/SakuraAlphaArduino)

### Blog (Japanese)
http://android.ohwada.jp/archives/7077
