# WebSocket Client - SAKURA IoT Platform Alpha

## Node-RED
Parse the mesage from SAKURA IoT Platform <br/>
And display data in line chart <br/>

### Requirement 
[node-red](http://nodered.org/) <br/>
[node-red-contrib-googlechart](https://www.npmjs.com/package/node-red-contrib-googlechart) <br/>

### Sensor
HDC1000 temperature and humidity sensor <br/>
[datasheet](http://www.ti.com/product/HDC1000/datasheet)  <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/docs/sakura_iot_hdc1000.png" width="500" />

### Flow
- flow.js <br/>
- parser.js <br/>
parse the received data in WebSocket node, and convert to csv format <br/>
- text.js <br/>
sort in reverse order, from new data to old data <br/>
- temperature.js <br/>
select the latest 100 of data, and convert the graph format <br/>
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/ws_client/node-red/nodered_flow.png" width="300" />

### Result
<img src="https://github.com/ohwada/sakura_iot_alpha/blob/master/ws_client/node-red/nodered_temperature.png" width="500" />

### Blog (Japanese)
http://android.ohwada.jp/archives/7253
