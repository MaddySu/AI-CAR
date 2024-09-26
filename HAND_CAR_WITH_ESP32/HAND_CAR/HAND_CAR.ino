#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define led0 18
#define led1 19  //0
#define led2 23
#define led3 13
#define led4 0
#define led5 2
#define led6 4
#define led7 5

#define i2c_Address 0x3c //initialize with the I2C addr 0x3C Typically eBay OLED's


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1    // QT-PY / XIAO
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

DynamicJsonDocument jsonBuffer(1024);

const char *ssid = "Robokidz_ESP";         // Set the ESP32 AP SSID
const char *password = "Robo1234";    // Set the ESP32 AP password
const int serverPort = 80;                  // Set the port number

int sensorValue0 = 0;
int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int sensorValue4 = 0;

String sensor_values;

WebServer server(serverPort);

void handleSentVar() {
  if (server.hasArg("sensor_reading")) {
    sensor_values = server.arg("sensor_reading");
    Serial.println(sensor_values);

    DeserializationError error = deserializeJson(jsonBuffer, sensor_values);
    if (!error) {
      sensorValue0 = jsonBuffer["sensor0_reading"];
      sensorValue1 = jsonBuffer["sensor1_reading"];
      sensorValue2 = jsonBuffer["sensor2_reading"];
      sensorValue3 = jsonBuffer["sensor3_reading"];
      sensorValue4 = jsonBuffer["sensor4_reading"];

    } else {
      Serial.println("Failed to parse JSON");
    }
  }

  Serial.println(sensorValue0);
  Serial.println(sensorValue1);
  Serial.println(sensorValue2);
  Serial.println(sensorValue3);
  Serial.println(sensorValue4);

  toggle_leds();
  update_display();

  server.send(200, "text/html", "Data received");
}

void setup() {
  Serial.begin(9600);
  pinMode(led0, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  pinMode(led6, OUTPUT);
  pinMode(led7, OUTPUT);

    digitalWrite(led4, LOW);
    digitalWrite(led5, LOW);
    digitalWrite(led6, LOW);
    digitalWrite(led7, LOW);

  // Configure ESP32 as access point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");
  Serial.print("IP Address: ");  
  Serial.println(WiFi.softAPIP());

  server.on("/data/", HTTP_GET, handleSentVar);
  server.begin();
  
  delay(250); // wait for the OLED to power up
  if(!display.begin(i2c_Address, true)) { // Address 0x3C default
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
}

void loop() {
  server.handleClient();
}

void toggle_leds() {
  // digitalWrite(led0, sensorValue0 >= 1 ? HIGH : LOW);
  // digitalWrite(led1, sensorValue1 >= 2 ? HIGH : LOW);
  // digitalWrite(led2, sensorValue2 >= 3 ? HIGH : LOW);
  // digitalWrite(led3, sensorValue3 >= 4 ? HIGH : LOW);
  // digitalWrite(led4, sensorValue4 >= 5 ? HIGH : LOW);
  if(sensorValue0 == 5)
  {
    digitalWrite(led0, LOW);
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);

  }
     else if (sensorValue0 == 4)
  {
    digitalWrite(led0, HIGH);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, HIGH);
    digitalWrite(led4, LOW);

  }
       else if (sensorValue0 == 3)
  {
    digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);

  }
        else if (sensorValue0 == 2)
  {
    digitalWrite(led0, LOW);
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);

  }
        else if (sensorValue0 == 1)
  {
   digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);

  }
        else if (sensorValue0 == 0)
  {
    digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
    digitalWrite(led4, LOW);

  }
}

void update_display() {
  display.clearDisplay();
  display.setTextSize(2);       // Increase text size to 2:1 pixel scale
  display.setTextColor(SH110X_WHITE); // Draw white text

  const char* message = "";

  if (sensorValue0 == 6) {
    message = "NEUTRAL";
  } 
  else if (sensorValue0 == 5) 
  {
    message = "SURPRISE";
  } 
  else if (sensorValue0 == 4) 
  {
    message = "FEAR";
  } 
  else if (sensorValue0 == 3) 
  {
    message = "SED";
  } 
  else if (sensorValue0 == 2) 
  {
    message = "ANGRY";
  } 
  else if (sensorValue0 == 1) 
  {
    message = "HAPPY";
  }

  int16_t x1, y1;
  uint16_t w, h;
  display.getTextBounds(message, 0, 0, &x1, &y1, &w, &h);
  int16_t x = (SCREEN_WIDTH - w) / 2;
  int16_t y = (SCREEN_HEIGHT - h) / 2;

  display.setCursor(x, y);
  display.println(message);
  display.display();
}
