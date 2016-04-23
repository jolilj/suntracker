import RPi.GPIO as GPIO
import time

from vservo import vServo
from hservo import hServo

GPIO.setmode(GPIO.BCM)
v_Servo = vServo(18, GPIO)
h_Servo = hServo(17, GPIO)

while True:
	u = float(raw_input('increment pos?: '))
	v_Servo.setPos(u)
	#h_Servo.setPos(c*0.1)
	print(u)

#for i in range(4,19):
#	pos = 0.0001*i*50*100
#	pwm.start(pos)
#	time.sleep(1)
#	print(pos)


GPIO.cleanup()

