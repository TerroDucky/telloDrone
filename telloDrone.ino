// Buttons
const int PinLedRight    = 2;
const int PinbuttonRight = 3;
const int PinLedLeft     = 4;
const int PinbuttonLeft  = 5;

const int PingUltLed     = 6;
const int PingUltButton  = 7;
const int UltButtonDelay = 5000;

// Joysticks
const int VertJoyY = A0;
const int VertJoyX = A1;

const int MoveJoyX = A2;
const int MoveJoyY = A3;

// Joystick calibration
int vertCenterX;
int vertCenterY;
int moveCenterX;
int moveCenterY;
int joystickCalibrationDelay = 1500;

const int deadzone = 40;

void setup() {
  Serial.begin(9600);
  // Right button
  pinMode(PinLedRight, OUTPUT);
  pinMode(PinbuttonRight, INPUT_PULLUP);
  // left button
  pinMode(PinLedLeft, OUTPUT);
  pinMode(PinbuttonLeft, INPUT_PULLUP);

  pinMode(PingUltLed, OUTPUT);
  pinMode(PingUltButton, INPUT_PULLUP);

  // Calibrate joysticks
  delay(joystickCalibrationDelay);
  vertCenterX = analogRead(VertJoyX);
  vertCenterY = analogRead(VertJoyY);
  moveCenterX = analogRead(MoveJoyX);
  moveCenterY = analogRead(MoveJoyY);
  
  Serial.println(" Setup completed ");
}

void loop() {

  // Right button
  if (digitalRead(PinbuttonRight) == LOW) {
    // Button is held down
    digitalWrite(PinLedRight, HIGH);
    Serial.println("ButtonRight");
  } else {
    digitalWrite(PinLedRight, LOW);
  }

  // Left button
  if (digitalRead(PinbuttonLeft) == LOW) {
    // Button is held down
    digitalWrite(PinLedLeft, HIGH);
    Serial.println("ButtonLeft");

  } else {
    digitalWrite(PinLedLeft, LOW);
  }

  // Ultimate button
  if (digitalRead(PingUltButton) == LOW) {
    // Button is held down
    digitalWrite(PingUltLed, LOW);
    Serial.println("UltimateButton");
    delay(UltButtonDelay);
  } else {
    digitalWrite(PingUltLed, HIGH);
  }

  // Vertical joystick
  int vertY = analogRead(VertJoyY);
  int vertX = analogRead(VertJoyX);

  if (abs(vertX - vertCenterX) > deadzone) {
    Serial.print("Vertical Joystick X: ");
    Serial.println(vertX);
  }

  if (abs(vertY - vertCenterY) > deadzone) {
    Serial.print("Vertical Joystick Y: ");
    Serial.println(vertY);
  }

  // Movement joystick
  int moveX = analogRead(MoveJoyX);
  int moveY = analogRead(MoveJoyY);

  if (abs(moveX - moveCenterX) > deadzone) {
    Serial.print("Movement Joystick X: ");
    Serial.println(moveX);
  }

  if (abs(moveY - moveCenterY) > deadzone) {
    Serial.print("Movement Joystick Y: ");
    Serial.println(moveY);
  }
}