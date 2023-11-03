//    motors:  1, 2,  3,  4
int pin1s[] = {2, 7, 10, 12};
int pin2s[] = {4, 8, 11, 13};
int pinPWMs[] = {3, 5, 6, 9}; // pin1, pin2, pwm pin
int speeds[] = {0, 0, 0, 0};

int motors = 4;
int minSpeed = 70;

void setup()
{ 
  // put your setup code here, to run once:
  Serial.setTimeout(10); // stops reading after 2ms
  for (int i = 0; i < motors; i++)
  {
    pinMode(pin2s[i], OUTPUT);
    pinMode(pin2s[i], OUTPUT);
  }
  
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int receivedValue = Serial.parseInt(); // Read and parse the integer from the serial input

    int motor = receivedValue % 10 - 1;
    Serial.print("Motor: ");
    Serial.println(motor);
    int speed = int(receivedValue/10);
    Serial.print("Speed: ");
    Serial.println(speed);

    setMotor(motor, speed);
  }

  // set speed
  // setMotor(motor1Pin1, motor1Pin2, motor1PinPWM, motor1Speed);

  // delay(100);
}

void setAllMotors(int speed)
{
  for (int i = 0; i < motors; i++)
  {
    setMotor(i, speed);
  }
}

void setMotor(int motor, int speed)
{
  if(motor == -1){
    return;
  }

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
    if(abs(speed) <= 255){
      analogWrite(pwmPin, abs(speed)); // from minSpeed-255
    }
  }
  else
  {
    analogWrite(pwmPin, 0);
  }
}
