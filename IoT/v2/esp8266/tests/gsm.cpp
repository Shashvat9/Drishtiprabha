#include <SoftwareSerial.h>
// Create software serial object to communicate with SIM900
// mySerial(7,8) for UNO, mySerial(D5,D6) in NodeMCU
SoftwareSerial mySerial(D6, D5);

void setup() {
  // Begin serial communication with Arduino UNO/NodeMCU and Arduino IDE (Serial Monitor)
  Serial.begin(9600);
  
  // Begin serial communication with Arduino and SIM900
  mySerial.begin(9600);
  Serial.println("Initializing...");
  delay(1000);
  
  // Initialize GSM module
  mySerial.println("AT"); // Handshake test
  updateSerial();
  
  mySerial.println("AT+CSQ"); // Signal quality test
  updateSerial();
  
  mySerial.println("AT+CCID"); // Read SIM information
  updateSerial();
  
  // Configure GSM module to notify on incoming SMS
  mySerial.println("AT+CNMI=2,2,0,0,0"); // Enable SMS notifications
  updateSerial();
  
  // Wait for network registration
  while (!isRegistered()) {
    Serial.println("Waiting for network registration...");
    delay(5000); // Wait 5 seconds before retrying
  }
  
  Serial.println("Network registered successfully.");
}

// void loop() {
//   updateSerial();
//   // Removed manual SMS checking since CNMI handles notifications
// }

void updateSerial() {
  delay(500);
  while (Serial.available()) {
    mySerial.write(Serial.read()); // Forward what Serial received to Software Serial Port
  }
  while (mySerial.available()) {
    Serial.write(mySerial.read()); // Forward what Software Serial received to Serial Port
  }
}

void receiveSMS(String smsContent) {
  Serial.println("Received SMS:");
  Serial.println(smsContent);
}

bool isRegistered() {
  mySerial.println("AT+CREG?");
  delay(500);
  
  while (mySerial.available()) {
    String response = mySerial.readStringUntil('\n');
    Serial.println(response); // For debugging
    
    if (response.indexOf("+CREG: 0,1") != -1 || response.indexOf("+CREG: 0,5") != -1) {
      return true;
    }
  }
  return false;
}

// Add a new function to parse incoming SMS
void parseIncomingSMS() {
  if (mySerial.available()) {
    String incoming = mySerial.readStringUntil('\n');
    if (incoming.indexOf("+CMT:") != -1) {
      String smsContent = mySerial.readStringUntil('\n');
      receiveSMS(smsContent);
    }
  }
}

// Modify the loop to handle incoming SMS notifications
void loop() {
  updateSerial();
  parseIncomingSMS();
}