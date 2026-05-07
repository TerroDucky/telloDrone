#include <Wire.h>
#include <rgb_lcd.h>

rgb_lcd lcd;

// ---------------- PINS ----------------
const int PinLedRight    = 2;
const int PinButtonRight = 3;
const int PinLedLeft     = 4;
const int PinButtonLeft  = 5;
const int PinUltLed      = 6;
const int PinUltButton   = 7;

const int VertJoyY = A0;
const int VertJoyX = A1;
const int MoveJoyX = A2;
const int MoveJoyY = A3;

// ---------------- CALIBRATION ----------------
int vertCenterX, vertCenterY, moveCenterX, moveCenterY;
bool lastR=false, lastL=false, lastU=false;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  lcd.begin(16,2);
  lcd.setRGB(255,255,255);

  pinMode(PinButtonRight, INPUT_PULLUP);
  pinMode(PinButtonLeft,  INPUT_PULLUP);
  pinMode(PinUltButton,   INPUT_PULLUP);
  pinMode(PinLedRight, OUTPUT);
  pinMode(PinLedLeft,  OUTPUT);
  pinMode(PinUltLed,   OUTPUT);

  lcd.print("Calibrating");
  delay(1500);

  vertCenterX = analogRead(VertJoyX);
  vertCenterY = analogRead(VertJoyY);
  moveCenterX = analogRead(MoveJoyX);
  moveCenterY = analogRead(MoveJoyY);

  lcd.clear();
  lcd.print("Ready");
}

void loop() {
  handleButton(PinButtonRight, PinLedRight, "R", lastR);
  handleButton(PinButtonLeft,  PinLedLeft,  "L", lastL);
  handleButton(PinUltButton,   PinUltLed,   "U", lastU);

  sendJoy("VX", VertJoyX);
  sendJoy("VY", VertJoyY);
  sendJoy("MX", MoveJoyX);
  sendJoy("MY", MoveJoyY);

  delay(20); // 50 Hz
}

void handleButton(int btn, int led, const char* lbl, bool &last) {
  bool p = digitalRead(btn) == LOW;
  digitalWrite(led, p ? HIGH : LOW);
  if (p != last) {
    Serial.print("BTN:");
    Serial.print(lbl);
    Serial.println(p ? ":DOWN" : ":UP");
    last = p;
  }
}

void sendJoy(const char* lbl, int pin) {
  Serial.print("JOY:");
  Serial.print(lbl);
  Serial.print(",");
  Serial.println(analogRead(pin));
}