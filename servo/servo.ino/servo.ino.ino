int value = 0;
int direction = 1;
int servoPin = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(value == 255 || value == -255){
    direction *= -1;
  }
  value += direction;

  analogWrite(servoPin, value);
  Serial.println(value);

  delay(50);
}
