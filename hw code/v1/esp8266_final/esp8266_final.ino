#include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <WiFiClient.h>
  #include <string.h>
  #include <UniversalTelegramBot.h>
  #include <ArduinoJson.h>
  #include <WiFiClientSecure.h>

  //for giolocation

  #include <Arduino.h>
  #if defined ARDUINO_ARCH_ESP8266
  #include <ESP8266WiFi.h>
  #elif defined ARDUINO_ARCH_ESP32
  #include <WiFi.h>
  #else
  #error Wrong platform
  #endif
  #include <WifiLocation.h>

  #if __has_include("wificonfig.h")
  #include "wificonfig.h"
  #else

const char* ssid     = "Hi";
const char* password = "hithere.";
const String serverName = "https://3.108.54.205/api/v2/update_db.php";
const char* googleApiKey = "";
String apiKeyValue = "dp123";
String d_id = "dp1"

#endif
WifiLocation location (googleApiKey);


// Initialize Telegram BOT
#define BOTtoken ""  // your Bot Token (Get from Botfather)


#define CHAT_ID "5511379301" //shashvat
// #define CHAT_ID "1638809558" //aryan

#define CHAT_ID ""
// #define CHAT_ID ""

X509List cert(TELEGRAM_CERTIFICATE_ROOT);
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

const int motionSensor = 14; // PIR Motion Sensor
bool motionDetected = false;

// Indicates when motion is detected
void ICACHE_RAM_ATTR detectsMovement() {
  //Serial.println("MOTION DETECTED!!!");
  motionDetected = true;
}

void setup() {
  Serial.begin(9600);

  configTime(0, 0, "pool.ntp.org");      // get UTC time via NTP
  client.setTrustAnchors(&cert); // Add root certificate for api.telegram.org

  // PIR Motion Sensor mode INPUT_PULLUP
  pinMode(motionSensor, INPUT_PULLUP);
  // Set motionSensor pin as interrupt, assign interrupt function and set RISING mode
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);

  // Attempt to connect to Wifi network:
  wifi_connect();

  //for giolocation

  configTime (0, 0, "pool.ntp.org", "time.nist.gov");

    Serial.print ("Waiting for NTP time sync: ");
    time_t now = time (nullptr);
    while (now < 8 * 3600 * 2) {
        delay (500);
        Serial.print (".");
        now = time (nullptr);
    }
    struct tm timeinfo;
    gmtime_r (&now, &timeinfo);
    Serial.print ("\n");
    Serial.print ("Current time: ");
    Serial.print (asctime (&timeinfo));

  bot.sendMessage(CHAT_ID, "Hello this is a bot for drishtiprabha. you will recive all emergency notifications heare.", "");//sends message to boat

}

void loop() {
    location_t loc = location.getGeoFromWiFi();
     if (WiFi.status() == WL_CONNECTED) {
       if(motionDetected){
          String location_message="I need help this is my loaction- https://www.google.com/maps/search/" + String (loc.lat, 6) + "," + String (loc.lon, 6); 
          send_alert(String (loc.lon, 6),String (loc.lat, 6));
          // String location_message="I need help this is my loaction- https://www.google.com/maps/search/21.718863,72.121439"; 
          bot.sendMessage(CHAT_ID,location_message, "");
          motionDetected = false;
        }
     }
}

void wifi_connect()
{
  Serial.print("Connecting Wifi: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void send_alert(String lon,String lat)
{
  HTTPClient http;
        WiFiClientSecure wificlint;
        wificlint.setInsecure();
        String httpRequestData = "?api_key="+apiKeyValue+"&longitude="+lon+"&latitude="+lat+"&d_id="+d_id;
        // String httpRequestData="I need help this is my loaction- https://www.google.com/maps/search/" + lat + "," + lon; 
        // int longitude=5566;
        // int latitude=6655;

        http.addHeader(":authority", "drishtiprabha.000webhostapp.com");
        http.addHeader(":method", "GET");
      //  http.addHeader(":path", "/update_db.php?api_key=dp123&latitude=21.726541&longitude=71.966305&add=dp1");
       http.addHeader(":path", "/update_db.php?api_key=dp123&latitude="+lat+"&longitude="+lon+"&add=dp1");
       http.addHeader(":scheme", "https");
        http.addHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7");
        http.addHeader("Accept-Encoding", "gzip, deflate, br");
        http.addHeader("Accept-Language", "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,gu;q=0.6");
        http.addHeader("Cache-Control", "max-age=0");
        http.addHeader("Sec-Ch-Ua", "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"");
        http.addHeader("Sec-Ch-Ua-Mobile", "?0");
        http.addHeader("Sec-Ch-Ua-Platform", "\"Windows\"");
        http.addHeader("Sec-Fetch-Dest", "document");
        http.addHeader("Sec-Fetch-Mode", "navigate");
        http.addHeader("Sec-Fetch-Site", "none");
        http.addHeader("Sec-Fetch-User", "?1");
        http.addHeader("Upgrade-Insecure-Requests", "1");
//        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        http.addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36");
        // http.addHeader("Cookie", "__test=fad13ccfd536b9e6f2bb446873411e6d");
        http.addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 ");

        Serial.print("httpRequestData: ");
        Serial.println(httpRequestData);
        Serial.print("url: ");
        Serial.println(serverName + httpRequestData.c_str());

        http.begin(wificlint,serverName + httpRequestData.c_str());

        int httpResponseCode = http.GET();

        if (httpResponseCode > 0) {
          Serial.print("HTTP Response code: ");
          Serial.println(httpResponseCode);
          Serial.println();
          
        }
        else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
        }
        // Free resources
        http.end();
}
