// SAKURA IoT - Serial
// connect Arduino monitor to the serial port of iot module
// 2016-06-20 K.OHWADA

#include <AltSoftSerial.h>
AltSoftSerial altSerial;

// Board          Transmit  Receive   PWM Unusable
// Arduino Uno        9         8         10

#define SERIAL_SPEED 9600
#define ALT_SPEED 115200

void setup() {
    Serial.begin( SERIAL_SPEED );
    altSerial.begin( ALT_SPEED );
    Serial.println("start");
}

void loop() {
    if ( Serial.available() ) {
        altSerial.write( Serial.read() );
    }
    if ( altSerial.available() ) {
        int c = altSerial.read();
        Serial.write( c );
    }	
}
