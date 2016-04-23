import time
import math
class vServo:
	def __init__(self, pin, gpio):
		self.pin = pin
		self.gpio = gpio
		self.gpio.setup(pin,gpio.OUT)
		self.pwm=gpio.PWM(pin,50)
		self.pwm.start(0)
		self.pos = 100
		self.setPos(50)
		time.sleep(0.5)
		print("vServo initialized!")

	def setPos(self,pos):
		dutyCycle = posToPWM(pos)
		self.pwm.ChangeDutyCycle(dutyCycle)
		print("dutycycle: " + str(dutyCycle))
		#t = math.fabs(self.pos - pos)*1
		#time.sleep(t)
		#self.pwm.start(0)
		self.pos = pos

#pos between 0 and 100
def posToPWM(pos):
	d = -0.035*pos+8.5
	return d