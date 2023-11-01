int motor1Pin1 = 2;
int motor1Pin2 = 3;
int motor1PinPWM = 9;
int motor1Speed = 0;

int minSpeed = 60;

char endChar = "n";

void setup() {
  // put your setup code here, to run once:
  Serial.setTimeout(10); //stops reading after 2ms
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int receivedValue = Serial.parseInt(); // Read and parse the integer from the serial input
    // You can now use the receivedValue as an integer
    if(abs(motor1Speed) < 256){
      motor1Speed = receivedValue;
    }
  }

  //set speed
  setMotor(motor1Pin1, motor1Pin2, motor1PinPWM, motor1Speed);

  //delay(100);
}

void setMotor(int pin1, int pin2, int pwmPin, int speed){
  //direction
  if(speed > 0){
    digitalWrite(pin1, HIGH);  
    digitalWrite(pin2, LOW);
  }
  else{
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
  }

  //speed set
  if(abs(speed) > minSpeed){
    analogWrite(pwmPin, abs(speed)); //from minSpeed-255
  }
  else{
    analogWrite(pwmPin, 0);
  }
}
