 /*
    HTTP over TLS (HTTPS) example sketch

    This example demonstrates how to use
    WiFiClientSecure class to access HTTPS API.
    We fetch and display the status of
    esp8266/Arduino project continuous integration
    build.

    Limitations:
      only RSA certificates
      no support of Perfect Forward Secrecy (PFS)
      TLSv1.2 is supported since version 2.4.0-rc1

    Created by Ivan Grokhotkov, 2015.
    This example is in public domain.
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
WiFiClient client;
String url;
const char* ssid = "RT-WiFi-3308";
const char* password = "29102005";
String id = "1";
String state = "0";
int rele = 5;
const char* host = "xsestech.tk";
const int httpPort = 80;
String name = "lamp1";
String dev_type = "lamp";
void setup() {
  Serial.begin(115200);
  pinMode(5, OUTPUT);
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
   delay(1);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Use WiFiClient class to create TLS connection
  WiFiClient client;
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  url = "/buy-elephant/esp8266/" + id + "/" + name + "/" + dev_type+ "/" + state;
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: ESP8266\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("request sent");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  if (line == "1")  {
    state == "1";
    digitalWrite(5, HIGH);
    Serial.println("on");
  } else if(line == "0") {
    state == "0";
    digitalWrite(5, LOW);
    Serial.println("off");
  } else{
    Serial.println("FAIL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
  }
  Serial.println("reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("closing connection");
  
}

void loop() {
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  url = "/buy-elephant/esp8266/" + id + "/" + state;
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: ESP8266\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("request sent");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  if (line == "1") {
    state == "1";
    digitalWrite(5, HIGH);
    Serial.println("on");
    
  } else if(line == "0") {
    state == "0";
    digitalWrite(5, LOW);
    Serial.println("==========");
    Serial.println("off");
    Serial.println("==========");
  } else{
    Serial.println("FAIL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
  }
  Serial.println("reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("closing connection");
}
