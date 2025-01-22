#include <SoftwareSerial.h>      //Include Serial Communication Library
//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(8, 12);  //Define Serial Tx and Rx pins , SIM800L Tx & Rx is connected to Arduino #8 & #12

//set up code Run Once
void setup() {
  Serial.begin(9600);     //Begin serial communication at 9600 Baud Rate with Arduino and Arduino IDE (Serial Monitor)
  mySerial.begin(9600);   //Begin serial communication with Arduino and SIM800L

  //Initialize
  Serial.println("Initializing...");
  delay(1000);
  SerialCMD("AT");          //First HandShake Test
  SerialCMD("AT+CMGF=1");   // Configuring TEXT mode
  SerialCMD("AT+CMGS=\"+918153841347\"");//send sms
  delay(1000);
  mySerial.print("Hello this is SMS Testing From SIM808");
    delay(1000);
   // Read and print the MSG
  while (mySerial.available()) {
    Serial.write(mySerial.read()); // Forward what Software Serial received to Serial Port
  }
  mySerial.write(26);  //ESC Character Indicating Terminate the MSG
}

//Main Code Continuous Loop
void loop() {
  //Do Nothing
}

void SerialCMD(String command) {
  mySerial.println(command); // Send the AT command
  delay(1000); // Wait for the response
  // Read and print the response
  while (mySerial.available()) {
    Serial.write(mySerial.read()); // Forward what Software Serial received to Serial Port
  }
}
