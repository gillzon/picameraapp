import RPi.GPIO as GPIO
import time

while True:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(18,GPIO.OUT)
	print("led on")
	GPIO.output(18,GPIO.HIGH)
	time.sleep(3)
	print("led off")
	GPIO.output(18,GPIO.OUT)
	time.sleep(3)
