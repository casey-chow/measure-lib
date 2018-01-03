#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

void setup() {
  Serial.begin(115200);
  

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  Serial.println("Adafruit VL53L0X test");

  pinMode(12, OUTPUT); // left
  pinMode(13, OUTPUT); // right

  // #1
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  delay(10);
  digitalWrite(13, HIGH);
  digitalWrite(12, HIGH);
  delay(10);

  // #2/3/4
  Serial.println("booting left");
  digitalWrite(12, LOW);
  if (!lox.begin(0x30, true)) {
    Serial.println(F("Failed to boot VL53L0X Left"));
    while(1);
  }

  // #5u
  Serial.println("booting right");
  digitalWrite(12, HIGH);
  if (!lox2.begin(0x31, true)) {
    Serial.println(F("Failed to boot VL53L0X Right"));
    while(1);
  }
  
  // power 
  Serial.println(F("VL53L0X API Simple Ranging example\n\n")); 
  
}


void loop() {
  VL53L0X_RangingMeasurementData_t measure;
    
  Serial.print("Reading... \n");
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
  
  if (measure.RangeStatus != 4 && measure.RangeMilliMeter >= 30) {  // phase failures have incorrect data
    Serial.print("\tDistance (mm): "); Serial.print(measure.RangeMilliMeter); 
  } else {
    Serial.print("\t out of range ");
  }

  
  lox2.rangingTest(&measure, false);
    
  if (measure.RangeStatus != 4 && measure.RangeMilliMeter >= 30) {  // phase failures have incorrect data
    Serial.print("\tDistance (mm): "); Serial.print(measure.RangeMilliMeter); 
  } else {
    Serial.print ("\t out of range ");
  }

  Serial.println("");
    
  delay(100);
}
