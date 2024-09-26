#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
// Makes a finger wave to test the servos
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 200
#define SERVOMAX 550

void setup() {
  Serial.begin(9600);
  pwm1.begin();
  pwm1.setPWMFreq(60);
}


void loop() {
  //closing loop 
  for (int finger_num = 0; finger_num < 5; finger_num++){ // assuming the left-most finger is 0, then fingers in order
      pwm1.setPWM(finger_num, 0, SERVOMIN);
      delay(100);
  }

  // opening loop
  for (int finger_num = 0; finger_num < 5; finger_num++){ // assuming the left-most finger is 0, then fingers in order
      pwm1.setPWM(finger_num, 0, SERVOMAX);
      delay(100);
  }

  delay(800);
}
