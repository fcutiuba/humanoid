#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Allows for a single finger to move to a desired pulse length
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 180 // Min and max pulse length allowed
#define SERVOMAX 700

uint8_t servonum = 3; // The number servo on the PWM board, change to your desired number

void setup() {
  Serial.begin(9600);
  pwm1.begin();
  pwm1.setPWMFreq(60);

  Serial.println("Enter pulse length (180 to 700):");
}

void loop() { // waits for input, then moves the finger
  if (Serial.available()) {  
    int pulse = Serial.parseInt();  

    if (pulse >= SERVOMIN && pulse <= SERVOMAX) {  
      pwm1.setPWM(servonum, 0, pulse);  
      Serial.print("Pulse set to: ");
      Serial.println(pulse);
    } else {
      Serial.println("Invalid pulse length. Please enter a value between 180 and 700.");
    }

    Serial.println("Enter next pulse length (180 to 700):");
  }
  delay(100);  
}