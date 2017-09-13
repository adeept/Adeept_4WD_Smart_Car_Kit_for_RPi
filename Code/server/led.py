#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LedPin = 31  # 29/31/33

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led

def loop():
	for i in range(1, 3):
		setup()
		GPIO.output(LedPin, GPIO.LOW)  # led on
		time.sleep(0.5)
		setup()
		GPIO.output(LedPin, GPIO.HIGH) # led off
		time.sleep(0.5)

def stop(LedPin):
	GPIO.output(LedPin, GPIO.HIGH)     # led off

def destroy():
	stop(LedPin)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()


