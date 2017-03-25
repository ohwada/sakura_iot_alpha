# SAKURA IoT Platform Alpha
Programs for SAKURA IoT Platform Alpha
### Total System
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_fab_sensor_android_watch.png" width="500" />

### Arduino
- sakura_iot_fab_sensor <br/>
  Send data obtained from sensors to Sakura IoT Platform <br/>
- sakura_iot_serial <br/>
  Connect Arduino monitor to the serial port of Sakura IoT comm board <br/>
- SakuraAlpha_I2C_with_hdc1000 <br/>
  https://github.com/sakura-internet/SakuraAlphaArduino/tree/master/examples/SakuraAlpha_I2C_with_hdc1000 <br/>

### Server
- python: sakura_iot_fab_sensor <br/>
  Web app display sensor data in graph <br/>

### Android
  display sensor values on android phone and android watch<br/>

### WebSocket Client
- JavaScript <br/>
  Parse the mesage from SAKURA IoT Platform <br/>
- Python <br/>
  Parse the mesage from SAKURA IoT Platform <br/>
- Node-RED <br/>
  Parse the mesage from SAKURA IoT Platform <br/>
  And display data in line chart <br/>

### Wiring connection to Arduino

|Sakura IoT|Arduino|
|---|---|
|1 UART TX (O)|D8 or D0|
|2 UART RX (I)|D9 or D1|
|3 GND|GND|
|4 SPI MOSI (I)|D11|
|5 SPI MISO (O)|D12|
|6 SPI SCK (I)|D13|
|7 SPI CS (I)|D10|
|8 GND|GND|
|9 I2C SDA (I/O)|SDA (A4)|
|10 I2C SCL (I/O)|SCK (A5)|
|11 GND|GND|
|12 +5V|+5V|

### Case
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_case_board.png" width="500" />

### Blog (Japanese)
- http://android.ohwada.jp/archives/7077
- http://android.ohwada.jp/archives/7045
