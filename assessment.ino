#include <Wire.h>
#include <SparkFun_APDS9960.h>

SparkFun_APDS9960 apds = SparkFun_APDS9960();

void setup() {
  Serial.begin(9600);

  if (apds.init()) {
    Serial.println("APDS-9960 initialized");
  } else {
    Serial.println("Failed to init sensor");
    while (1);
  }

  if (apds.enableGestureSensor(true)) {
    Serial.println("Gesture sensor ready");
  } else {
    Serial.println("Gesture sensor failed");
    while (1);
  }
}

void loop() {
  if (apds.isGestureAvailable()) {
    int gesture = apds.readGesture();

    switch (gesture) {
      case DIR_LEFT:
        Serial.println("LEFT");
        break;
      case DIR_RIGHT:
        Serial.println("RIGHT");
        break;
      case DIR_UP:
        Serial.println("UP");
        break;
      case DIR_DOWN:
        Serial.println("DOWN");
        break;
      case DIR_NEAR:
        Serial.println("FORWARD");
        break;
      case DIR_FAR:
        Serial.println("BACKWARD");
        break;
      default:
        Serial.print("Unknown gesture code: ");
        Serial.println(gesture);
    }
    
    // Small delay to prevent gesture spam
    delay(100);
  }
}

