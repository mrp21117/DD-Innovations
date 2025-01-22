#include <SoftwareSerial.h>      //Include Serial Communication Library
//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(8, 12);  //Define Serial Tx and Rx pins , SIM800L Tx & Rx is connected to Arduino #8 & #13

void myFunction() {
  Serial.println("Checking Parameters"); // Print a message
  SerialCMD("AT");            //First HandShake Test
  SerialCMD("ATI");           //Check Module and Version
  SerialCMD("AT+IPR=9600");   //Set Baud rate
  SerialCMD("AT+CSQ");        //Check Signal Quality
  SerialCMD("AT+CSDT=1");     //start SIMCARD Detection Function
  SerialCMD("AT+CCID");       //Check SIMCARD Valid or Not
  SerialCMD("AT+CREG?");      //Check SIMCARD Registered or Not
  SerialCMD("AT+COPS?");      //Check Connected Network Operator
  Serial.println("Initalize Successful");  
}

//set up code Run Once
void setup() {
  Serial.begin(9600);     //Begin serial communication at 9600 Baud Rate with Arduino and Arduino IDE (Serial Monitor)
  mySerial.begin(9600);   //Begin serial communication with Arduino and SIM800L

  //Initialize
  Serial.println("Initializing...");
  myFunction(); // Call the custom function
  delay(1000); // Allow time for GSM module to initialize
}

void loop() {
  // put your main code here, to run repeatedly:
}


void SerialCMD(String command) {
  mySerial.println(command); // Send the AT command
  delay(1000); // Wait for the response
  // Read and print the response
  while (mySerial.available()) {
    Serial.write(mySerial.read()); // Forward what Software Serial received to Serial Port
  }
}
