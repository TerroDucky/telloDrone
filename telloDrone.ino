const int PinLedRight    = 2;
const int PinbuttonRight = 3;
const int PinLedLeft     = 4;
const int PinbuttonLeft  = 5;

void setup() {
  Serial.begin(9600);
  // Right button
  pinMode(PinLedRight, OUTPUT);
  pinMode(PinbuttonRight, INPUT_PULLUP);
  // left button
  pinMode(PinLedLeft, OUTPUT);
  pinMode(PinbuttonLeft, INPUT_PULLUP);

  Serial.println(" Setup completed ");

}

void loop() {
// Buttons

  // Right button
  if (digitalRead(PinbuttonRight) == LOW) {
    // Button is held down
    digitalWrite(PinLedRight, HIGH);
    Serial.println("ButtonRight");
  } else { // Button is not held down
    digitalWrite(PinLedRight, LOW);
  }

  // Left button
  if (digitalRead(PinbuttonLeft) == LOW) {
    // Button is held down
    digitalWrite(PinLedLeft, HIGH);
    Serial.println("ButtonLeft");
  } else { // Button is not held down
    digitalWrite(PinLedLeft, LOW);
  }

}
