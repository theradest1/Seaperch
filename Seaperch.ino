#include <Servo.h>
Servo vexServo;

int armPin = 2;

//    motors:  1, 2,  3,  4
int pin1s[] = {22, 7, 10, 12};
int pin2s[] = {4, 8, 11, 13};
int pinPWMs[] = {3, 5, 6, 9}; // pin1, pin2, pwm pin


// motor 1 = front
// motor 2 = back
// motor 3 = left
// motor 4 = right

int motors = 4;
int minSpeed = 100; // so they dont stall and burn out

bool stringEnded = false;
char stringDelimiter = '\n';
String stringBuilder = "";

void setup()
{

  vexServo.attach(armPin);

  // set used pins to output
  for (int i = 0; i < motors; i++)
  {
    pinMode(pin1s[i], OUTPUT);
    pinMode(pin2s[i], OUTPUT);
  }

  // initialize communication
  Serial.begin(6000);

}

void loop()
{
  
}

void setMotor(int motor, int speed)
{ 
  //01000100010001000100
  /*Serial.print(motor);
  Serial.print(" - ");
  Serial.println(speed);*/

  if (motor == -1)
  {
    return;
  }
  if (motor == 4){
    vexServo.write(speed);
  }
  else{
    int pin1 = pin1s[motor];
    int pin2 = pin2s[motor];
    int pwmPin = pinPWMs[motor];

    // direction
    if (speed > 0)
    {
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, LOW);
    }
    else
    {
      digitalWrite(pin1, LOW);
      digitalWrite(pin2, HIGH);
    }

    // speed set
    if (abs(speed) > minSpeed)
    {
      if (abs(speed) <= 255)
      {
        analogWrite(pwmPin, abs(speed)); // from minSpeed-255
      }
    }
    else
    {
      analogWrite(pwmPin, 0);
    }
  }

  // Serial.println("Set motor " + String(motor) + " to " + String(speed));
}
