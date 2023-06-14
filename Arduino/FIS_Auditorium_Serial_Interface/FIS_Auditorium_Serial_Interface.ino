#include <Wire.h>
int dmxValues[5];
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(12, OUTPUT);    //Relay 1 (PJ Screen)
  pinMode(11, OUTPUT);    //Relay 2 (Other)
  
  //DMX pins are inputs be default

  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // function that executes whenever data is received from writer
  pinMode(LED_BUILTIN,OUTPUT);  // sets onBoard LED as output
}
String data = "";
String temp = "";
void loop() {
  char a = Serial.read();
  if (a=='S') {
    digitalWrite(12, HIGH);
    delay(700);
    digitalWrite(12, LOW);
    
  }
  if (a=='N') {
    digitalWrite(11, HIGH);
  }
  if (a=='F') {
    digitalWrite(11, LOW);
  }
}
void receiveEvent(int howMany)
{
  temp=data;
  data = "";
  while( Wire.available()){
    data += (char)Wire.read();
    if(temp!=data){
      Serial.println(data);
    }
  }
}
