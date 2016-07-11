/**
 * Fab Sensor with Sakura IoT Board
 * Temperature, Humidity, Air Pressure, Light, Noise
 *
 * 2016-07-01 K.OHWDA
 */ 

/*
 * require
 * Arduino Library for the DHT11
 *   https://github.com/adafruit/DHT-sensor-library
 * Driver for the Adafruit MPL115A2 barometric pressure sensor breakout
 *   https://github.com/adafruit/Adafruit_MPL115A2
 */

/**
 * send data
 * ch0: temperature
 * ch1: humidity
 * ch2: pressure
 * ch3: light
 * ch4: noise
 */

/**
 * Sensor Device
 * Temperature & Humidity : DHT11
 * Air Pressure : MPL115A2
 * Light : NJL7502L
 * Noise : Microphone C9767BB422LFP
 */

#include <SakuraAlpha.h>
#include <Wire.h>
#include <Adafruit_MPL115A2.h>
#include <DHT.h>

// Pins
#define PIN_DHT  3
#define PIN_LED  9
#define PIN_LIGHT  A0
#define PIN_NOISE  A1
// A4 (SDA), A5 (SCL) of I2C
// for MPL115A2 and Sakura IoT Board

// Sensor   
#define DHTTYPE  DHT11   // DHT 11 
#define UNDIFINED_VALUE  -1
#define NOISE_OFFSET 512
#define AVARAGE_NUM  100
#define COFF_LIGHT  0.78 # value -> Lux

#define SERIAL_SPEED  9600
#define TIME_LOOP  500  // 0.5 sec
#define TIME_SEND  60000  // 60 sec

// class
DHT dht( PIN_DHT, DHTTYPE );
Adafruit_MPL115A2 mpl115a2;
SakuraAlphaI2C sakura;

// led blink
boolean g_led_status = false;

// time when send data
unsigned long g_time_send = 0;

/**
 * === setup ===
 */
void setup() {
	// Initialize Serial port
	Serial.begin( SERIAL_SPEED );
	Serial.println();
	Serial.println( F("---------------------------") );
	Serial.println( F("FabLab Kannai Sensor Project") );
	Serial.println( F("---------------------------") );

    	// GPIO setting
	pinMode( PIN_LED, OUTPUT );	
	dht.begin();
	mpl115a2.begin();
	
    // waiting connect
    Serial.println("Waiting to come online...");
    while (1) {
        // break, if connected
        if( sakura.getNetworkStatus() == 1 ) break;
        delay(1000);
    }	    
}

/**
 * === loop ===
 */
void loop() {  
    // send every 60 sec
    	unsigned long now = millis();
    	if (( (now - g_time_send) > TIME_SEND )|| 
        ( now < g_time_send )) {
        // after 60 sec
        // or millis() is overflowed
		g_time_send = now;
		sendData();
	}  
	// blink LED
	g_led_status = !g_led_status;
	if ( g_led_status ) {
		digitalWrite( PIN_LED, HIGH );
	} else {
  		digitalWrite( PIN_LED, LOW );
	}
	// wait 0.5 sec
	delay( TIME_LOOP ); 
}

/**
 * sendData
 */
void sendData() {
    // --- read sensor ---
	float values[2];
    readTemperatureHumidity( values );	
    float temp = values[0];
  	float humi = values[1];
    float pressure = readPressure();
    float light = readLight();
    float noise = readNoise();
    sendSerial( temp, humi, pressure, light, noise );
    // write
    sakura.writeChannel(0, temp);
    sakura.writeChannel(1, humi);
    sakura.writeChannel(2, pressure);
    sakura.writeChannel(3, light);
    sakura.writeChannel(4, noise);
    // transmit
    sakura.transmit(TRANSMIT_ONCE);
}

/**
 * read Temperature Humidity
 */
void readTemperatureHumidity( float* values ) {
    float temp = dht.readTemperature();
  	float humi = dht.readHumidity();
  	// Check if any reads failed
  	if ( isnan(temp) || isnan(humi) ) {
        	temp = UNDIFINED_VALUE;
		humi = UNDIFINED_VALUE;
		Serial.println( F("Failed to read from DHT sensor!") );
  	}
  	values[0] = temp;
  	values[1] = humi;  	
}

/**
 * read Pressure
 */
float readPressure() {
    float pressure = 10 * mpl115a2.getPressure();
    return pressure;
}

/**
 * read Light
 */
float readLight() {
    int light_raw = analogRead( PIN_LIGHT );
    float light = COFF_LIGHT * (float)light_raw;
    return light;
}

/**
 * read Noise  
 */   
float readNoise() {
    float noise_raw = readAnalogAverage( PIN_NOISE );
    float noise = abs( noise_raw - NOISE_OFFSET );
    return noise;
}
    
/**
 * readAnalogAverage
 */
float readAnalogAverage( int pin ) {
	long total = 0;
	for( int i=0; i < AVARAGE_NUM; i++ ) {
		total += analogRead( pin );
	}
	float average = (float)total / AVARAGE_NUM;  
	return average;
}

/**
 * sendSerial
 */
void sendSerial( float temp, float humi, float pressure, float light, float noise ) {
	Serial.print( "temperature:" );
	Serial.print( temp );
	Serial.print( ", humidity:" );
	Serial.print( humi );
	Serial.print( ", pressure:" );
	Serial.print( pressure );
	Serial.print( ", light:" );
	Serial.print( light );
	Serial.print( ", noise:" );
	Serial.print( noise );
	Serial.println();
}
