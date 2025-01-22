#include <ESP8266WiFi.h>

// Access Point credentials
const char* ssid = "ESP8266";
const char* password = "12345678";

WiFiServer server(80); // Create a server on port 80

// GPIO pins for LEDs
const int gpioPins[4] = {16, 5, 4, 0}; // GPIO 16 (D0), GPIO 5 (D1), GPIO 4 (D2), GPIO 0 (D3)

void setup() {
  Serial.begin(115200);

  // Set GPIO pins as outputs and turn them off
  for (int i = 0; i < 4; i++) {
    pinMode(gpioPins[i], OUTPUT);
    digitalWrite(gpioPins[i], HIGH);
  }

  // Set up Access Point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");

  // Print the ESP8266 IP address
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP Address: ");
  Serial.println(IP);

  // Start the server
  server.begin();
  Serial.println("Server Started");
}

void loop() {
  // Check if a client is connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Wait for the client to send data
  while (!client.available()) {
    delay(1);
  }

  // Read the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Process button actions for each GPIO
  for (int i = 0; i < 4; i++) {
    if (request.indexOf("/LED" + String(i + 1) + "_ON") != -1) {
      Serial.println("LED " + String(i + 1) + " ON");
      digitalWrite(gpioPins[i], LOW);
    }
    if (request.indexOf("/LED" + String(i + 1) + "_OFF") != -1) {
      Serial.println("LED " + String(i + 1) + " OFF");
      digitalWrite(gpioPins[i], HIGH);
    }
  }

  // Respond with a dashboard HTML page
  String response =
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Connection: close\r\n\r\n"
    "<!DOCTYPE HTML>"
    "<html>"
    "<head>"
    "<title>ESP8266 Dashboard</title>"
    "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    "<style>"
    "body { font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 0; background-color: #f4f4f4; }"
    "h1 { color: #333; margin: 20px; }"
    ".button { display: block; width: 80%; max-width: 300px; margin: 10px auto; padding: 15px; border: none; border-radius: 5px; background-color: #007BFF; color: white; font-size: 18px; cursor: pointer; transition: background-color 0.3s, box-shadow 0.3s; }"
    ".button:hover { background-color: #0056b3; }"
    ".button.glow { background-color: #007BFF; box-shadow: 0px 0px 10px 3px #007BFF; }"
    "</style>"
    "<script>"
    "function toggleLED(id, state) {"
    "  const button = document.getElementById('ledButton' + id);"
    "  if (state === 'ON') {"
    "    button.classList.add('glow');"
    "    fetch('/LED' + id + '_ON');"
    "  } else {"
    "    button.classList.remove('glow');"
    "    fetch('/LED' + id + '_OFF');"
    "  }"
    "}"
    "</script>"
    "</head>"
    "<body>"
    "<h1>ESP8266 Dashboard</h1>"
    "<h3>Control Panel</h3>"
    "<button id='ledButton1' class='button' onclick=\""
    "this.classList.toggle('glow');"
    "if (this.classList.contains('glow')) { toggleLED(1, 'ON'); } else { toggleLED(1, 'OFF'); }"
    "\">Toggle LED 1</button>"
    "<button id='ledButton2' class='button' onclick=\""
    "this.classList.toggle('glow');"
    "if (this.classList.contains('glow')) { toggleLED(2, 'ON'); } else { toggleLED(2, 'OFF'); }"
    "\">Toggle LED 2</button>"
    "<button id='ledButton3' class='button' onclick=\""
    "this.classList.toggle('glow');"
    "if (this.classList.contains('glow')) { toggleLED(3, 'ON'); } else { toggleLED(3, 'OFF'); }"
    "\">Toggle LED 3</button>"
    "<button id='ledButton4' class='button' onclick=\""
    "this.classList.toggle('glow');"
    "if (this.classList.contains('glow')) { toggleLED(4, 'ON'); } else { toggleLED(4, 'OFF'); }"
    "\">Toggle LED 4</button>"
    "</body>"
    "</html>";
  client.print(response);

  // Close the connection
  delay(1);
}
