int servoPin = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  analogWrite(servoPin, 0);
  Serial.println("255");
  delay(1000);
  analogWrite(servoPin, 255);
  Serial.println("255");
  delay(1000);
}
