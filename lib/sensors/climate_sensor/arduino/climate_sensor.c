#include <dht22.h>
#include <dht11.h>

#define DHTPIN 4

void setup() {
  // initialize both serial ports:
  Serial.begin(56000);
}

void loop() {
  // read from port 0, send to port 1:
  while(1){
    int chk = DHT11.read(DHTPIN);
    Serial.print((float)DHT11.humidity, 2);
    Serial.print(",");
    Serial.print((float)DHT11.temperature, 2);
    Serial.print("\n");
  }
}
