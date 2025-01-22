#include <SoftwareSerial.h>

SoftwareSerial mySerial(4, 3); // RX, TX

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() // run over and over
{
  // SEND COMMAND
    while (Serial.available())
    {
      mySerial.write(Serial.read());
    }
  
  //GETTING RESPONSE
  while (mySerial.available())
  {
    Serial.write(mySerial.read());
  }
}
