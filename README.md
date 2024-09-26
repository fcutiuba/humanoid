# Humanoid Robot Test Suite

This test suite is designed for testing servos on a humanoid robot. It includes three Arduino programs to help you verify the functionality of your robot's hand servos.

## Table of Contents
1. [Installation](#installation)
2. [Programs](#programs)
   - [Finger Wave](#finger-wave)
   - [Finger Wave with Reversed Finger](#finger-wave-with-reversed-finger)
   - [Single Finger Move](#single-finger-move)

## Installation

1. Ensure you have the Arduino IDE installed on your computer.
2. Install the following libraries in your Arduino IDE:
   - `Wire.h` (should be included with Arduino IDE)
   - `Adafruit_PWMServoDriver.h` (can be installed via the Library Manager)
3. Connect your Arduino board to the PWM servo driver (default address: 0x40).
4. Connect your servos to the PWM servo driver.

## Programs

### Finger Wave

File: `finger-wave.ino`

This program makes the hand perform a finger wave to test all servos.

#### Usage
1. Upload the `finger-wave.ino` file to your Arduino board.
2. The program will continuously loop through all fingers, closing and then opening them in sequence.

#### Customization
- Modify `SERVOMIN` and `SERVOMAX` values to adjust the range of motion for your specific servos.
- Change the `delay` values to adjust the speed of the wave.

### Finger Wave with Reversed Finger

File: `finger-wave-reversed-finger.ino`

Similar to the basic finger wave, but accounts for one finger (the 4th) having reversed polarity.

#### Usage
1. Upload the `finger-wave-reversed-finger.ino` file to your Arduino board.
2. The program will perform a finger wave, with the 4th finger (index 3) moving in the opposite direction.

#### Customization
- Modify the `if (finger_num == 3)` condition to change which finger is considered reversed.
- Adjust `SERVOMIN` and `SERVOMAX` values as needed for your servos.

### Single Finger Move

File: `single_finger_move.ino`

This program allows you to move a single finger/servo to a specific position using serial input.

#### Usage
1. Upload the `single_finger_move.ino` file to your Arduino board.
2. Open the Serial Monitor in the Arduino IDE (set baud rate to 9600).
3. Enter a pulse length between 180 and 700 to move the servo.

#### Customization
- Change the `servonum` variable to test different servo positions on the PWM board.
- Modify `SERVOMIN` and `SERVOMAX` to set the allowable range for your servos.

## General Notes

- All programs use the Adafruit PWM Servo Driver with the default address (0x40). If you're using a different address, update the `Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);` line in each program.
- The finger numbering assumes the left-most finger is 0, with fingers numbered in order from left to right.
- Always ensure your power supply can handle the current draw of all connected servos.

## Troubleshooting

If you encounter issues:
1. Check all connections between the Arduino, PWM driver, and servos.
2. Verify that you've installed the required libraries.
3. Ensure the PWM driver address matches your hardware setup.
4. Adjust the `SERVOMIN` and `SERVOMAX` values if your servos aren't moving through their full range.
