import RPi.GPIO as GPIO
import time
import pygame
import pygame.camera
from pygame.locals import *
from thresh_image import ThreshImage
import math

from Servo import Servo


#init camera
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

image = cam.get_image()
im = ThreshImage(pygame.image.tostring(image,"RGBA",False),640,480)
im.thresh(230)
im.image.convert('RGB').save("images/image2.jpg")