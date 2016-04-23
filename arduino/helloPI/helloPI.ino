#include <Servo.h>

// pins
#define VSERVO_PIN 3
#define HSERVO_PIN 5

//hservo working range 10-160
//vservo working range 40-120
#define HSERVO_MIN 10
#define HSERVO_MAX 160
#define VSERVO_MIN 40
#define VSERVO_MAX 120

// Map horizontal servo control signal to 0-149 ASCII
// and vertical servo control signal to 150-230
#define U_H_MAX 149.0 
#define U_V_MAX 80.0 //230.0-150

#define uToHPos(u) (HSERVO_MAX-HSERVO_MIN)/U_H_MAX*u + HSERVO_MIN
#define uToVPos(u) (VSERVO_MAX-VSERVO_MIN)/U_V_MAX*u + VSERVO_MIN

Servo vServo;
Servo hServo;
void setup() {
  vServo.attach(VSERVO_PIN);
  hServo.attach(HSERVO_PIN);
  Serial.begin(9600);
}

void loop() {
  Serial.begin(9600);
  if (Serial.available()){
    int u = Serial.read();
    int pos = 90; // default
    if (u > 149) { //control signal is for vertical servo
      u = u-149;
      pos = uToVPos(u);
      pos = pos > VSERVO_MAX ? VSERVO_MAX : pos;
      pos = pos < VSERVO_MIN ? VSERVO_MIN : pos;
      vServo.write(pos); 
    } else { // control signal is for horizontal servo
      pos = uToHPos(u);
      pos = pos > HSERVO_MAX ? HSERVO_MAX : pos;
      pos = pos < HSERVO_MIN ? HSERVO_MIN : pos;
      hServo.write(pos);
    }
    
  }
  delay(1000);

}
