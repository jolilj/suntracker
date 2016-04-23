#include <Servo.h>

#define SERVO_PIN 3
//hservo working range 10-160
//vservo working range 40-120
#define HSERVO_MIN 10
#define HSERVO_MAX 160
#define VSERVO_MIN 40
#define VSERVO_MAX 120

#define uToVPos(u) (VSERVO_MAX-VSERVO_MIN)/100.0*u + VSERVO_MIN
#define uToHPos(u) (HSERVO_MAX-HSERVO_MIN)/100.0*u + HSERVO_MIN

Servo hServo;

void setup() {
  Serial.begin(9600);
  //hServo.attach(3);

}

void loop() {
  for(int u=0; u<=100; u+=10) {
    Serial.println(u);
    Serial.println(uToVPos(u));
    delay(1000);
  }

}
