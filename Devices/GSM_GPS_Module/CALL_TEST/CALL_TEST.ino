#include <SoftwareSerial.h>      //Include Serial Communication Library
//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(8, 12);  //Define Serial Tx and Rx pins , SIM800L Tx & Rx is connected to Arduino #8 & #13

//set up code Run Once
void setup() {
  Serial.begin(9600);     //Begin serial communication at 9600 Baud Rate with Arduino and Arduino IDE (Serial Monitor)
  mySerial.begin(9600);   //Begin serial communication with Arduino and SIM800L

  //Initialize
  Serial.println("Initializing...");
  delay(1000);
  mySerial.println("AT");      //AT Command to Check  //Once the handshake test is successful, it will back to OK
  printSerialData();
  delay(1000);
  mySerial.println("AT+CSQ");      //AT Command to Check  //Once the handshake test is successful, it will back to OK
  printSerialData();
  delay(1000);
  mySerial.println("AT+COPS?");      //AT Command to Check  //Once the handshake test is successful, it will back to OK
  printSerialData();
  delay(1000);
  mySerial.println("AT+CREG?");      //AT Command to Check  //Once the handshake test is successful, it will back to OK
  printSerialData();
  delay(1000);
}

int MissCall = 1;
//Main Code Continuous Loop
void loop() {
  while(MissCall){
  //Make a Call Once
  mySerial.println("ATD+918153841347;"); //Dial the Phone Number
  delay(20000); // wait for 20 seconds...
  mySerial.println("ATH"); //hang up
  printSerialData();
  delay(1000);
  --MissCall;
  }
}

//Function to Print Received Serial DATA
void printSerialData()
{
  delay(500);
  while (Serial.available())
  {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while (mySerial.available())
  {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}
