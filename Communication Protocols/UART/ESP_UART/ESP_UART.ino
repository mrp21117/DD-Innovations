#include <SoftwareSerial.h>

// Define custom RX and TX pins for SoftwareSerial
#define RX_PIN 4  // GPIO4 (D2 on NodeMCU)
#define TX_PIN 5  // GPIO5 (D1 on NodeMCU)

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Create a SoftwareSerial instance

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(115200); 
  delay(1000); // Stabilize before starting
  Serial.println("ESP8266 Custom Pins Serial Communication Initialized");

  // Initialize SoftwareSerial
  mySerial.begin(115200); 
  Serial.println("SoftwareSerial ready. Type a message in Serial Monitor to send via TX.");
}

void loop() {
  // **1. Transmit Data**: Read from Serial Monitor and send to TX_PIN
  if (Serial.available()) {
    String dataToSend = Serial.readStringUntil('\n'); // Read from Serial Monitor
    mySerial.println(dataToSend); // Send to SoftwareSerial TX_PIN
    Serial.println("Sent to SoftwareSerial TX: " + dataToSend); // Debug message
  }

  // **2. Receive Data**: Read from RX_PIN and display on Serial Monitor
  if (mySerial.available()) {
    String receivedData = mySerial.readStringUntil('\n'); // Read from SoftwareSerial RX_PIN
    Serial.println("Received on SoftwareSerial RX: " + receivedData); // Print to Serial Monitor
  }

  delay(100); // Small delay for stability
}
