#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
// Does the finger wave, but one of the hands has the "polarity" of the 4th finger reversed
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN 200
#define SERVOMAX 550

uint8_t servonum = 0;

void setup() {
  Serial.begin(9600);
  pwm1.begin();
  pwm1.setPWMFreq(60);
}

void loop() {
  //closing loop 
  for (int finger_num = 0; finger_num < 5; finger_num++){ // assuming the left-most finger is 0, then fingers in order
    if (finger_num == 3){
      pwm1.setPWM(finger_num, 0, SERVOMAX);
      delay(100);
    }
    else{
      pwm1.setPWM(finger_num, 0, SERVOMIN);
      delay(100);
    }
  }

  // opening loop
  for (int finger_num = 0; finger_num < 5; finger_num++){ // assuming the left-most finger is 0, then fingers in order
    if (finger_num == 3){
      pwm1.setPWM(finger_num, 0, SERVOMIN);
      delay(100);
    }
    else{
      pwm1.setPWM(finger_num, 0, SERVOMAX);
      delay(100);
    }
  }

  delay(800);
}
