#include <ESP8266WiFi.h>        // Include the Wi-Fi library

const char* ssid     = "ESP8266";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "ESP12345";     // The password of the Wi-Fi network



void setup() {
  Serial.begin(115200);
  int numberOfNetworks = WiFi.scanNetworks();
  for (int i = 0; i < numberOfNetworks; i++) {
    Serial.print("Network name: ");
    Serial.println(WiFi.SSID(i));
  }

  delay(100);
  Serial.println('\n');

  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }
  Serial.println('\n');
  Serial.println("Network Connected");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer
}
void loop() {
  // put your main code here, to run repeatedly:
}
