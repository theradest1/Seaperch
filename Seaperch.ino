//    motors:  1, 2,  3,  4
int pin1s[] = {2, 7, 10, 12};
int pin2s[] = {4, 8, 11, 13};
int pinPWMs[] = {3, 5, 6, 9}; // pin1, pin2, pwm pin

// motor 1 = front
// motor 2 = back
// motor 3 = left
// motor 4 = right

int motors = 4;
int minSpeed = 60; // so they dont stall and burn out

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
    // Serial.println("Received thing: " + stringBuilder);

    // split string into parts
    String strSpeeds[] = {"", "", "", ""};
    for (int i = 0; i < stringBuilder.length(); i++)
    {
      char currentChar = stringBuilder.charAt(i);
      int currentSpeed = int(i / 4);
      strSpeeds[currentSpeed] += currentChar;
    }

    // parse each string into an int
    for (int i = 0; i < 4; i++)
    {

      // load string
      String unparsedSpeed = strSpeeds[i];

      // change N to negative
      unparsedSpeed.replace('N', '-');

      // remove leading zeros
      if (unparsedSpeed.startsWith("0"))
      {
        int j = 0;
        while (j < unparsedSpeed.length() && unparsedSpeed.startsWith("0"))
        {
          unparsedSpeed.remove(j, 1);
          j++;
        }
      }

      // convert to int and use
      setMotor(i, unparsedSpeed.toInt());
    }

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

  // Serial.println("Set motor " + String(motor) + " to " + String(speed));
}
