
#include <SoftwareSerial.h>

// defines pins numbers
const int trigPin = 9;
const int echoPin = 8;
const int vibrate = 5;
const int messagepin = 3;
// defines variables
long duration;
int distance;
int SPEAKER = 4;
const int BUTTON_PIN = 7; // Arduino pin connected to button's pin
int buttonState;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication
  pinMode(SPEAKER, OUTPUT);
  pinMode(vibrate, OUTPUT);
}
void loop() {

  buttonState = digitalRead(BUTTON_PIN); // read new state
  // Clears the trigPin condition
  buttonState = HIGH;
  
  if (buttonState == LOW) {
    delay(5000);
    digitalWrite(SPEAKER,HIGH);
    digitalWrite(messagepin, HIGH);
    digitalWrite(messagepin, LOW);
    // Serial.println("hi");    
  }

  else if (buttonState == HIGH)
  {
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance = duration * 0.034 / 2;
    // Prints the distance on the Serial Monitor
    
    Serial.print("Distance: ");
    Serial.println(distance);

    // Displays the distance on the Serial Monitor
    if(distance<=100 && distance >=70)
    {
      digitalWrite(vibrate,HIGH);
        tone(SPEAKER,100);
      // digitalWrite(SPEAKER,HIGH);
        delay(100);
        // digitalWrite(SPEAKER,LOW);
        noTone(SPEAKER);
        delay(100);
    }
    else if(distance<70 && distance >=40)
    {
      //  tone(SPEAKER,50);
      digitalWrite(SPEAKER,HIGH);
        delay(50);
        // noTone(SPEAKER);
        digitalWrite(SPEAKER,LOW);
        delay(50);
    }
    else if(distance<40 && distance >=10)
    {  
      //  tone(SPEAKER,25);
      digitalWrite(SPEAKER,HIGH);
        delay(20);
      // noTone(SPEAKER);
        digitalWrite(SPEAKER,LOW);
      
      delay(20);
    }

    else if(distance<10)
    {
      //  tone(SPEAKER,1000);
        digitalWrite(SPEAKER,HIGH);
        delay(0);
        // noTone(SPEAKER);   
    }    
  }
  
}