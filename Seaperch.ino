//    motors:  1, 2,  3,  4
int pin1s[] = {2, 7, 10, 12};
int pin2s[] = {4, 8, 11, 13};
int pinPWMs[] = {3, 5, 6, 9}; // pin1, pin2, pwm pin
int speeds[] = {0, 0, 0, 0};

// motor 1 = front
// motor 2 = back
// motor 3 = left
// motor 4 = right

int motors = 4;
int minSpeed = 80; // so they dont stall and burn out

bool stringEnded = false;
char stringDelimiter = '\n';
String stringBuilder = "";

void setup()
{
  // set used pins to output
  for (int i = 0; i < motors; i++)
  {
    pinMode(pin1s[i], OUTPUT);
    pinMode(pin2s[i], OUTPUT);
  }

  // initialize communication
  Serial.begin(9600);
}

void loop()
{
  // keep reading stream while things are there
  while (Serial.available() > 0)
  {
    // get next character
    char incomingByte = Serial.read();

    if (incomingByte == stringDelimiter)
    {
      // end building if hits end of string
      stringEnded = true;
    }
    else
    {
      // otherwise add the next charto the builder
      stringBuilder += incomingByte;
    }
  }

  // process if hit string end
  if (stringEnded)
  {
    // debug
    Serial.println("Received String: " + stringBuilder);

    // reset builder and flag
    stringBuilder = "";
    stringEnded = false;
  }
}

void setMotor(int motor, int speed)
{
  if (motor == -1)
  {
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
