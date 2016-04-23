import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera
from pygame.locals import *
from thresh_image import ThreshImage
import math

from hservo import hServo
from vservo import vServo

SLEEP_TIME = 5
DELTA_T = 0.3
ERROR_TOL = 0.04
WIDTH = 320
HEIGHT = 240
IMAGE_CENTER  = [int(WIDTH/2), int(HEIGHT/2)]
K1 = 20
K2 = 12

def cleanUp(e):
	print(e)
	GPIO.cleanup()

#init servos
GPIO.setmode(GPIO.BCM)
v_Servo = vServo(18, GPIO)
h_Servo = hServo(17, GPIO)

#init camera
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(WIDTH,HEIGHT))
cam.start()

try:
     #collect data in file
	fx = open("datax.txt", "w")
	fy = open("datay.txt", "w")
	while True:
		image = cam.get_image()
		pygame.image.save(image, 'images/pre_image.jpg')
		errorx = ERROR_TOL
		errory = ERROR_TOL
		#control loop
		t_x = 0
		while math.fabs(errorx) >= ERROR_TOL:
			t_x += 1
			print("t_x: ")
			print(t_x)
			image = cam.get_image()
			im = ThreshImage(pygame.image.tostring(image,"RGBA",False),WIDTH,HEIGHT)
			im.thresh(230)
			sunCenter = im.getCenterOfMass()
			#im.image.putpixel((sunCenter[0],sunCenter[1]),150)
			#im.image.putpixel((sunCenter[0]+1,sunCenter[1]+1),150)
			#im.image.putpixel((sunCenter[0]-1,sunCenter[1]+1),150)
			#im.image.putpixel((sunCenter[0]+1,sunCenter[1]-1),150)
			#im.image.putpixel((sunCenter[0]-1,sunCenter[1]-1),150)

			#im.image.convert('RGB').save("images/temp_image" + str(c) + ".jpg")
			print("Sun center")
			print(sunCenter)
			px_error = IMAGE_CENTER[0]-sunCenter[0]
			print("px_error: " + str(px_error))
			errorx = float(px_error)/WIDTH
			ux = int(h_Servo.pos + K1*errorx)
			if (ux < 0):
				ux = 0
			print("Control signal: ")
			print("x: " + str(ux))
			h_Servo.setPos(ux)

			print("Error in x:")
			print(errorx)
			print("==============================")
			print("==============================")
			fx.write(str(t_x) + "," + str(errorx) + "," + str(ux) + "\n")
			time.sleep(DELTA_T)
		print("=========== X DONE ===========")
		print("==============================")
		t_y = 0
		while math.fabs(errory) >= ERROR_TOL:
			t_y += 1
			print("t_y: ")
			print(t_y)
			image = cam.get_image()
			im = ThreshImage(pygame.image.tostring(image,"RGBA",False),WIDTH,HEIGHT)
			im.thresh(230)
			sunCenter = im.getCenterOfMass()
			#im.image.putpixel((sunCenter[0],sunCenter[1]),150)
			#im.image.putpixel((sunCenter[0]+1,sunCenter[1]+1),150)
			#im.image.putpixel((sunCenter[0]-1,sunCenter[1]+1),150)
			#im.image.putpixel((sunCenter[0]+1,sunCenter[1]-1),150)
			#im.image.putpixel((sunCenter[0]-1,sunCenter[1]-1),150)

			#im.image.convert('RGB').save("images/temp_image" + str(c) + ".jpg")
			print("Sun center")
			print(sunCenter)
			py_error = sunCenter[1] - IMAGE_CENTER[1]
			print("py_error: " + str(py_error))
			errory = float(py_error)/HEIGHT
			uy = int(v_Servo.pos + K2*errory)
			if (uy < 0):
				uy = 0
			print("Control signal: ")
			print("y: " + str(uy))
			v_Servo.setPos(uy)

			print("Error in y:")
			print(errory)
			print("==============================")
			print("==============================")
			fy.write(str(t_y) + "," + str(errory) + "," + str(uy) + "\n")
			time.sleep(DELTA_T)
		print("=========== Y DONE ===========")
		print("==============================")

		image = cam.get_image()
		im = ThreshImage(pygame.image.tostring(image,"RGBA",False),WIDTH,HEIGHT)
		im.image.convert('RGB').save("images/post_image.jpg")
		im.thresh(230)


		sunCenter = im.getCenterOfMass()
		im.image.putpixel((sunCenter[0],sunCenter[1]),150)
		im.image.putpixel((sunCenter[0]+1,sunCenter[1]+1),150)
		im.image.putpixel((sunCenter[0]-1,sunCenter[1]+1),150)
		im.image.putpixel((sunCenter[0]+1,sunCenter[1]-1),150)
		im.image.putpixel((sunCenter[0]-1,sunCenter[1]-1),150)
		im.image.convert('RGB').save("images/post_image_thresh.jpg")

		cam.stop()
		break
		time.sleep(SLEEP_TIME)   
except Exception,e:
	cleanUp(e)
	

