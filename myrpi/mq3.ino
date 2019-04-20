/* MQ-3 sensor */
const int AOutPin = 0;  // MQ-3 AOUT
const int ControlPin = 3;  // RPi control

int value;
int control;

void setup() {
  Serial.begin(115200);
  pinMode(ControlPin, INPUT);
}

void loop()
{
  control = digitalRead(ControlPin);  // read control value from RPi (ControlPin)
  if (control == HIGH) {
    value = analogRead(AOutPin);  // read the analog value from the AOutPin pin
    Serial.println(value);  // print received value to serial
  }
  delay(200);
}
