#include <Servo.h>

Servo vexServo;  // Create a servo object to control the VEX servo

int servoPin = 3; // Change this to the pin where your servo signal wire is connected

void setup() {
  vexServo.attach(servoPin); // Attach the servo to the specified pin
}

void loop() {
  vexServo.write(0);
  delay(1000);    
  vexServo.write(130); 
  delay(1000);    
}