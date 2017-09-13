#! /usr/bin/python
import RPi.GPIO as GPIO
import time

Tr = 23
Ec = 24


def checkdist():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(Ec, GPIO.IN)
	GPIO.output(Tr, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(Tr, GPIO.LOW)
	while not GPIO.input(Ec):
		pass
	t1 = time.time()
	while GPIO.input(Ec):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

try:
	print 'Press Ctrl+C to end the program'
	while True:
		print 'Distance: %0.2f m' %checkdist()
		time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.cleanup()


